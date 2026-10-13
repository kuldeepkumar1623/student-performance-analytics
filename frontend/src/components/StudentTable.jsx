import React, { useState, useMemo } from 'react';
import { Search, ArrowUpDown, Filter } from 'lucide-react';

export default function StudentTable({ data }) {
  const [search, setSearch] = useState('');
  const [deptFilter, setDeptFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [gradeFilter, setGradeFilter] = useState('');
  const [sortField, setSortField] = useState('Average_Marks');
  const [sortOrder, setSortOrder] = useState('desc'); // 'asc' or 'desc'

  const handleSort = (field) => {
    if (sortField === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortOrder('desc');
    }
  };

  const filteredAndSortedData = useMemo(() => {
    return data
      .filter((s) => {
        const matchesSearch =
          s.Name.toLowerCase().includes(search.toLowerCase()) ||
          s.Student_ID.toLowerCase().includes(search.toLowerCase());
        const matchesDept = deptFilter === '' || s.Department === deptFilter;
        const matchesStatus = statusFilter === '' || s.Status === statusFilter;
        const matchesGrade = gradeFilter === '' || s.Grade === gradeFilter;

        return matchesSearch && matchesDept && matchesStatus && matchesGrade;
      })
      .sort((a, b) => {
        let valA = a[sortField];
        let valB = b[sortField];

        if (typeof valA === 'string') {
          return sortOrder === 'asc'
            ? valA.localeCompare(valB)
            : valB.localeCompare(valA);
        }

        return sortOrder === 'asc' ? valA - valB : valB - valA;
      });
  }, [data, search, deptFilter, statusFilter, gradeFilter, sortField, sortOrder]);

  return (
    <div className="table-card">
      <div className="table-header">
        <div>
          <h2 style={{ fontSize: '18px', fontWeight: 800 }}>
            Student Performance Records
          </h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '13px' }}>
            Showing {filteredAndSortedData.length} of {data.length} students
          </p>
        </div>

        <div className="table-controls">
          <div className="search-input-wrap">
            <Search size={16} />
            <input
              type="text"
              placeholder="Search by name or ID..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="search-input"
            />
          </div>

          <select
            value={deptFilter}
            onChange={(e) => setDeptFilter(e.target.value)}
            className="select-filter"
          >
            <option value="">All Departments</option>
            <option value="Computer Science">Computer Science</option>
            <option value="Data Science">Data Science</option>
            <option value="Information Technology">Information Technology</option>
          </select>

          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="select-filter"
          >
            <option value="">All Status</option>
            <option value="Pass">Pass</option>
            <option value="Fail">Fail</option>
          </select>

          <select
            value={gradeFilter}
            onChange={(e) => setGradeFilter(e.target.value)}
            className="select-filter"
          >
            <option value="">All Grades</option>
            <option value="A">Grade A</option>
            <option value="B">Grade B</option>
            <option value="C">Grade C</option>
            <option value="D">Grade D</option>
            <option value="E">Grade E</option>
            <option value="F">Grade F</option>
          </select>
        </div>
      </div>

      <div className="table-wrapper">
        <table className="student-table">
          <thead>
            <tr>
              <th onClick={() => handleSort('Student_ID')}>
                ID {sortField === 'Student_ID' && (sortOrder === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('Name')}>
                Name {sortField === 'Name' && (sortOrder === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('Department')}>
                Department {sortField === 'Department' && (sortOrder === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('Mathematics')}>
                Math {sortField === 'Mathematics' && (sortOrder === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('Python')}>
                Python {sortField === 'Python' && (sortOrder === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('Data_Science')}>
                Data Science {sortField === 'Data_Science' && (sortOrder === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('Attendance')}>
                Attendance {sortField === 'Attendance' && (sortOrder === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('Total_Marks')}>
                Total {sortField === 'Total_Marks' && (sortOrder === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('Average_Marks')}>
                Average {sortField === 'Average_Marks' && (sortOrder === 'asc' ? '↑' : '↓')}
              </th>
              <th>Grade</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {filteredAndSortedData.map((s) => (
              <tr key={s.Student_ID}>
                <td style={{ fontWeight: 600 }}>{s.Student_ID}</td>
                <td>{s.Name}</td>
                <td style={{ color: 'var(--text-secondary)' }}>{s.Department}</td>
                <td>{s.Mathematics.toFixed(1)}</td>
                <td>{s.Python.toFixed(1)}</td>
                <td>{s.Data_Science.toFixed(1)}</td>
                <td>{s.Attendance.toFixed(1)}%</td>
                <td style={{ fontWeight: 600 }}>{s.Total_Marks.toFixed(1)}</td>
                <td style={{ fontWeight: 700, color: 'var(--primary)' }}>
                  {s.Average_Marks.toFixed(2)}
                </td>
                <td>
                  <span className={`tag-badge grade-${s.Grade}`}>
                    {s.Grade}
                  </span>
                </td>
                <td>
                  <span
                    className={`tag-badge ${
                      s.Status === 'Pass' ? 'tag-pass' : 'tag-fail'
                    }`}
                  >
                    {s.Status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

