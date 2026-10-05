import React, { useEffect, useState } from 'react';
import { FileText, Clock, AlertTriangle, CheckCircle2, ChevronRight, RefreshCw, Building2, MapPin } from 'lucide-react';
import { getDashboardStats, listComplaints } from '../services/api';

interface TrackingDashboardProps {
  onSelectComplaint: (complaintId: string) => void;
}

export const TrackingDashboard: React.FC<TrackingDashboardProps> = ({ onSelectComplaint }) => {
  const [stats, setStats] = useState<any>(null);
  const [complaints, setComplaints] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('ALL');

  const fetchData = async () => {
    setLoading(true);
    try {
      const [s, c] = await Promise.all([getDashboardStats(), listComplaints()]);
      setStats(s);
      setComplaints(c);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const filteredComplaints = complaints.filter((c) => {
    if (filter === 'ALL') return true;
    if (filter === 'ACTIVE') return ['SUBMITTED', 'ACKNOWLEDGED', 'ASSIGNED', 'IN_PROGRESS'].includes(c.status);
    if (filter === 'ESCALATED') return c.status === 'ESCALATED';
    if (filter === 'RESOLVED') return ['RESOLVED', 'VERIFICATION_PENDING', 'VERIFIED_RESOLVED'].includes(c.status);
    return true;
  });

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'SUBMITTED':
      case 'ACKNOWLEDGED':
        return <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-blue-500/20 text-blue-300 border border-blue-500/30">Submitted</span>;
      case 'ASSIGNED':
      case 'IN_PROGRESS':
        return <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">In Progress</span>;
      case 'ESCALATED':
        return <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-rose-500/20 text-rose-300 border border-rose-500/30 animate-pulse">SLA Escalated</span>;
      case 'RESOLVED':
      case 'VERIFICATION_PENDING':
        return <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-500/20 text-amber-300 border border-amber-500/30">Verification Pending</span>;
      case 'VERIFIED_RESOLVED':
        return <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">Verified Resolved</span>;
      default:
        return <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-gray-500/20 text-gray-300 border border-gray-500/30">{status}</span>;
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
      {/* Top Header & Refresh */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Citizen Tracking Dashboard</h2>
          <p className="text-xs text-gray-400">Track real-time status progression, SLA deadlines & verification results</p>
        </div>
        <button
          onClick={fetchData}
          className="self-start sm:self-auto px-3.5 py-2 rounded-xl glass-panel hover:bg-gray-800 text-xs text-gray-300 flex items-center gap-2"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          Refresh Status
        </button>
      </div>

      {/* Metrics Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
        <div className="glass-panel p-5 rounded-2xl border border-gray-800">
          <span className="text-[10px] uppercase tracking-wider font-semibold text-gray-400">Total Issues</span>
          <div className="text-2xl font-extrabold text-white mt-1">{stats?.total_issues || 0}</div>
        </div>
        <div className="glass-panel p-5 rounded-2xl border border-gray-800">
          <span className="text-[10px] uppercase tracking-wider font-semibold text-blue-400">Submitted</span>
          <div className="text-2xl font-extrabold text-blue-400 mt-1">{stats?.submitted || 0}</div>
        </div>
        <div className="glass-panel p-5 rounded-2xl border border-gray-800">
          <span className="text-[10px] uppercase tracking-wider font-semibold text-indigo-400">In Progress</span>
          <div className="text-2xl font-extrabold text-indigo-400 mt-1">{stats?.in_progress || 0}</div>
        </div>
        <div className="glass-panel p-5 rounded-2xl border border-gray-800">
          <span className="text-[10px] uppercase tracking-wider font-semibold text-rose-400">SLA Escalated</span>
          <div className="text-2xl font-extrabold text-rose-400 mt-1">{stats?.escalated || 0}</div>
        </div>
        <div className="glass-panel p-5 rounded-2xl border border-gray-800 col-span-2 lg:col-span-1">
          <span className="text-[10px] uppercase tracking-wider font-semibold text-emerald-400">Verified Resolved</span>
          <div className="text-2xl font-extrabold text-emerald-400 mt-1">{stats?.resolved || 0}</div>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-2 border-b border-gray-800 pb-3">
        {['ALL', 'ACTIVE', 'ESCALATED', 'RESOLVED'].map((tab) => (
          <button
            key={tab}
            onClick={() => setFilter(tab)}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
              filter === tab
                ? 'bg-indigo-600 text-white shadow-md'
                : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/50'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Complaint Cards Grid */}
      {filteredComplaints.length === 0 ? (
        <div className="glass-panel rounded-2xl p-12 text-center text-gray-400 text-sm">
          No complaints found in this view. Use "Report Issue" or run the "Demo Scenario".
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredComplaints.map((c) => (
            <div
              key={c.id}
              onClick={() => onSelectComplaint(c.id)}
              className="glass-card rounded-2xl p-6 cursor-pointer flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="font-mono text-xs font-bold text-indigo-400">{c.complaint_number}</span>
                  {getStatusBadge(c.status)}
                </div>

                <h3 className="text-base font-bold text-white mb-2">{c.category}</h3>
                
                <div className="space-y-1.5 text-xs text-gray-400 mb-4">
                  <div className="flex items-center gap-1.5">
                    <Building2 className="w-3.5 h-3.5 text-gray-500" />
                    <span>{c.department_name}</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <MapPin className="w-3.5 h-3.5 text-gray-500" />
                    <span className="truncate">{c.address || c.ward}</span>
                  </div>
                </div>
              </div>

              <div className="pt-4 border-t border-gray-800/80 flex items-center justify-between text-xs text-gray-400">
                <span className="text-[11px] text-gray-500">
                  {new Date(c.created_at).toLocaleDateString()}
                </span>
                <span className="text-indigo-400 font-semibold flex items-center gap-1 group-hover:translate-x-1 transition-transform">
                  View Timeline & Verification
                  <ChevronRight className="w-3.5 h-3.5" />
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
