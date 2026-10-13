import React, { useState, useRef } from 'react';
import { UploadCloud, FileSpreadsheet, FileText, CheckCircle, AlertCircle, RefreshCw } from 'lucide-react';
import * as XLSX from 'xlsx';
import Papa from 'papaparse';
import * as pdfjsLib from 'pdfjs-dist';

// Configure pdfjs worker
pdfjsLib.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.js`;

export default function FileUploader({ onDataLoaded, onResetDefault }) {
  const [dragOver, setDragOver] = useState(false);
  const [loading, setLoading] = useState(false);
  const [activeFile, setActiveFile] = useState(null);
  const [errorMsg, setErrorMsg] = useState('');
  const fileInputRef = useRef(null);

  // Helper to re-compute academic performance metrics (Total, Average, Grade, Status)
  const processRawStudentRecords = (rawRecords) => {
    if (!Array.isArray(rawRecords) || rawRecords.length === 0) {
      throw new Error("No data records found in file.");
    }

    return rawRecords.map((row, index) => {
      // Normalize column names (case-insensitive & trim)
      const cleanObj = {};
      Object.keys(row).forEach((k) => {
        cleanObj[k.trim()] = row[k];
      });

      const studentId = cleanObj['Student_ID'] || cleanObj['Student ID'] || cleanObj['ID'] || `S${String(index + 1).padStart(3, '0')}`;
      const name = cleanObj['Name'] || cleanObj['Student Name'] || `Student ${index + 1}`;
      const department = cleanObj['Department'] || cleanObj['Dept'] || 'General';

      const math = parseFloat(cleanObj['Mathematics'] || cleanObj['Math'] || 0) || 0;
      const python = parseFloat(cleanObj['Python'] || 0) || 0;
      const ds = parseFloat(cleanObj['Data_Science'] || cleanObj['Data Science'] || cleanObj['DS'] || 0) || 0;
      const attendance = parseFloat(cleanObj['Attendance'] || 75.0) || 75.0;

      const total = math + python + ds;
      const avg = parseFloat((total / 3).toFixed(2));

      // Grading logic
      let grade = 'F';
      if (avg >= 90) grade = 'A';
      else if (avg >= 80) grade = 'B';
      else if (avg >= 70) grade = 'C';
      else if (avg >= 60) grade = 'D';
      else if (avg >= 40) grade = 'E';

      // Pass/Fail logic: min 40 in each subject
      const status = (math >= 40 && python >= 40 && ds >= 40) ? 'Pass' : 'Fail';

      return {
        Student_ID: studentId,
        Name: name,
        Department: department,
        Mathematics: math,
        Python: python,
        Data_Science: ds,
        Attendance: attendance,
        Total_Marks: total,
        Average_Marks: avg,
        Grade: grade,
        Status: status,
      };
    });
  };

  const handleFile = async (file) => {
    if (!file) return;
    setLoading(true);
    setErrorMsg('');

    const ext = file.name.split('.').pop().toLowerCase();

    try {
      if (ext === 'csv') {
        // Parse CSV using PapaParse
        Papa.parse(file, {
          header: true,
          skipEmptyLines: true,
          dynamicTyping: true,
          complete: (results) => {
            try {
              const processed = processRawStudentRecords(results.data);
              setActiveFile({ name: file.name, type: 'CSV', count: processed.length });
              onDataLoaded(processed, file.name);
            } catch (err) {
              setErrorMsg(err.message);
            } finally {
              setLoading(false);
            }
          },
          error: (err) => {
            setErrorMsg(`CSV Parsing error: ${err.message}`);
            setLoading(false);
          }
        });

      } else if (ext === 'xlsx' || ext === 'xls') {
        // Parse Excel using SheetJS
        const data = await file.arrayBuffer();
        const workbook = XLSX.read(data, { type: 'array' });
        const firstSheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[firstSheetName];
        const json = XLSX.utils.sheet_to_json(worksheet);

        const processed = processRawStudentRecords(json);
        setActiveFile({ name: file.name, type: 'Excel', count: processed.length });
        onDataLoaded(processed, file.name);
        setLoading(false);

      } else if (ext === 'pdf') {
        // Parse PDF using PDF.js
        const arrayBuffer = await file.arrayBuffer();
        const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
        const textLines = [];

        for (let i = 1; i <= pdf.numPages; i++) {
          const page = await pdf.getPage(i);
          const textContent = await page.getTextContent();
          
          // Group text items by y-coordinate (rough line grouping)
          const items = textContent.items;
          const lineMap = {};

          items.forEach(item => {
            const y = Math.round(item.transform[5]);
            if (!lineMap[y]) lineMap[y] = [];
            lineMap[y].push({ x: item.transform[4], str: item.str });
          });

          // Sort lines top to bottom
          const sortedY = Object.keys(lineMap).sort((a, b) => b - a);
          sortedY.forEach(y => {
            const lineItems = lineMap[y].sort((a, b) => a.x - b.x);
            const lineStr = lineItems.map(it => it.str).join('\t');
            if (lineStr.trim().length > 0) {
              textLines.push(lineStr);
            }
          });
        }

        if (textLines.length < 2) {
          throw new Error("Could not extract student records table from PDF.");
        }

        // Process tabular lines
        const headers = textLines[0].split('\t').map(h => h.trim());
        const rawJson = [];

        for (let r = 1; r < textLines.length; r++) {
          const cells = textLines[r].split('\t').map(c => c.trim()).filter(c => c !== '');
          if (cells.length >= 4) {
            const rowObj = {};
            // Map cells to headers
            headers.forEach((h, idx) => {
              rowObj[h] = cells[idx] || '';
            });
            rawJson.push(rowObj);
          }
        }

        const processed = processRawStudentRecords(rawJson);
        setActiveFile({ name: file.name, type: 'PDF', count: processed.length });
        onDataLoaded(processed, file.name);
        setLoading(false);

      } else {
        setErrorMsg(`Unsupported file type: .${ext}. Please upload a .csv, .xlsx, or .pdf file.`);
        setLoading(false);
      }
    } catch (err) {
      console.error(err);
      setErrorMsg(`Error reading file: ${err.message}`);
      setLoading(false);
    }
  };

  const onDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleReset = () => {
    setActiveFile(null);
    setErrorMsg('');
    if (fileInputRef.current) fileInputRef.current.value = '';
    onResetDefault();
  };

  return (
    <div style={{
      background: 'var(--bg-card)',
      borderRadius: '16px',
      padding: '24px',
      border: '1px solid var(--border)',
      boxShadow: 'var(--shadow-sm)',
      marginBottom: '28px'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h2 style={{ fontSize: '18px', fontWeight: 800, display: 'flex', alignItems: 'center', gap: '8px' }}>
            <UploadCloud size={22} color="#4f46e5" />
            Dataset Upload & Dynamic Analysis
          </h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '13px', marginTop: '2px' }}>
            Upload any student dataset in <strong>CSV</strong>, <strong>Excel (.xlsx)</strong>, or <strong>PDF</strong> format to analyze instantly.
          </p>
        </div>

        {activeFile && (
          <button
            onClick={handleReset}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '8px 14px',
              borderRadius: '8px',
              border: '1px solid var(--border)',
              background: 'var(--bg-primary)',
              cursor: 'pointer',
              fontSize: '13px',
              fontWeight: 600,
              color: 'var(--text-secondary)'
            }}
          >
            <RefreshCw size={14} />
            Reset to Default Dataset
          </button>
        )}
      </div>

      {/* Dropzone */}
      <div
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={onDrop}
        onClick={() => fileInputRef.current && fileInputRef.current.click()}
        style={{
          border: `2px dashed ${dragOver ? '#4f46e5' : '#cbd5e1'}`,
          borderRadius: '12px',
          padding: '28px 20px',
          textAlign: 'center',
          backgroundColor: dragOver ? '#eff6ff' : '#f8fafc',
          cursor: 'pointer',
          transition: 'all 0.2s ease',
        }}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv, .xlsx, .xls, .pdf"
          style={{ display: 'none' }}
          onChange={(e) => e.target.files && handleFile(e.target.files[0])}
        />

        <div style={{ display: 'flex', justifyContent: 'center', gap: '12px', marginBottom: '10px' }}>
          <span style={{ background: '#dbeafe', color: '#1d4ed8', padding: '6px 12px', borderRadius: '20px', fontSize: '12px', fontWeight: 700, display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
            <FileSpreadsheet size={14} /> CSV
          </span>
          <span style={{ background: '#d1fae5', color: '#047857', padding: '6px 12px', borderRadius: '20px', fontSize: '12px', fontWeight: 700, display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
            <FileSpreadsheet size={14} /> EXCEL (.xlsx)
          </span>
          <span style={{ background: '#fee2e2', color: '#b91c1c', padding: '6px 12px', borderRadius: '20px', fontSize: '12px', fontWeight: 700, display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
            <FileText size={14} /> PDF (.pdf)
          </span>
        </div>

        <p style={{ fontSize: '15px', fontWeight: 600, color: 'var(--text-primary)' }}>
          {loading ? 'Processing & Analyzing Dataset...' : 'Drag and drop your file here, or click to browse'}
        </p>
        <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '4px' }}>
          Supports students.csv, students.xlsx, students.pdf with columns: Student_ID, Name, Department, Mathematics, Python, Data_Science, Attendance
        </p>
      </div>

      {/* Error message */}
      {errorMsg && (
        <div style={{
          marginTop: '14px',
          padding: '10px 14px',
          borderRadius: '8px',
          background: '#fef2f2',
          border: '1px solid #fecaca',
          color: '#b91c1c',
          fontSize: '13px',
          display: 'flex',
          alignItems: 'center',
          gap: '8px'
        }}>
          <AlertCircle size={16} />
          {errorMsg}
        </div>
      )}

      {/* Active file status */}
      {activeFile && (
        <div style={{
          marginTop: '14px',
          padding: '10px 14px',
          borderRadius: '8px',
          background: '#f0fdf4',
          border: '1px solid #bbf7d0',
          color: '#15803d',
          fontSize: '13px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '8px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <CheckCircle size={16} />
            <span>Active Dataset: <strong>{activeFile.name}</strong> ({activeFile.type} format) • <strong>{activeFile.count} students analyzed</strong></span>
          </div>
          <span style={{ background: '#dcfce7', color: '#166534', padding: '2px 8px', borderRadius: '4px', fontSize: '11px', fontWeight: 700 }}>
            ANALYSIS UPDATED
          </span>
        </div>
      )}
    </div>
  );
}

