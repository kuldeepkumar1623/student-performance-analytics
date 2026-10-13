import React, { useState } from 'react';
import KPICards from './components/KPICards';
import ChartsSection from './components/ChartsSection';
import DepartmentBreakdown from './components/DepartmentBreakdown';
import StudentTable from './components/StudentTable';
import FileUploader from './components/FileUploader';
import initialStudentsData from './data/studentsData.json';
import { GraduationCap, Database } from 'lucide-react';

export default function App() {
  const [students, setStudents] = useState(initialStudentsData);
  const [datasetSource, setDatasetSource] = useState('Default (students.csv)');

  const handleDataLoaded = (newStudents, filename) => {
    setStudents(newStudents);
    setDatasetSource(filename);
  };

  const handleResetDefault = () => {
    setStudents(initialStudentsData);
    setDatasetSource('Default (students.csv)');
  };

  return (
    <div className="dashboard-container">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-title-box">
          <h1>
            <GraduationCap size={32} color="#4f46e5" />
            Student Performance Analytics
          </h1>
          <p>
            React Multi-Format Analytics • Ingests CSV, Excel (.xlsx) & PDF Datasets
          </p>
        </div>

        <div className="header-badges">
          <span className="badge-pill badge-react">
            <Database size={14} />
            {datasetSource}
          </span>
          <span className="badge-pill badge-status">
            <span className="pulse-dot"></span>
            Live Analytics
          </span>
        </div>
      </header>

      {/* Dataset File Upload & Format Selector */}
      <FileUploader
        onDataLoaded={handleDataLoaded}
        onResetDefault={handleResetDefault}
      />

      {/* KPI Cards */}
      <KPICards data={students} />

      {/* Charts Section */}
      <ChartsSection data={students} />

      {/* Department Breakdown */}
      <DepartmentBreakdown data={students} />

      {/* Student Roster Table */}
      <StudentTable data={students} />

      {/* Footer */}
      <footer>
        Student Performance Analytics System • Supports CSV, Excel & PDF Datasets • Built with React & Vite
      </footer>
    </div>
  );
}
