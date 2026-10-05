import React, { useEffect, useState } from 'react';
import { Settings, Play, ShieldAlert, Cpu, Activity, Clock, CheckCircle2, RefreshCw } from 'lucide-react';
import { getAuditLogs, getAgentExecutions, adminSimulateStatus, listComplaints } from '../services/api';

export const AdminControlPanel: React.FC = () => {
  const [complaints, setComplaints] = useState<any[]>([]);
  const [selectedComplaintId, setSelectedComplaintId] = useState<string>('');
  const [targetStatus, setTargetStatus] = useState<string>('IN_PROGRESS');
  const [notes, setNotes] = useState<string>('Hackathon judge demonstration fast-forward');
  
  const [auditLogs, setAuditLogs] = useState<any[]>([]);
  const [agentExecutions, setAgentExecutions] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);

  const fetchAdminData = async () => {
    setLoading(true);
    try {
      const [c, a, ex] = await Promise.all([
        listComplaints(),
        getAuditLogs(),
        getAgentExecutions(),
      ]);
      setComplaints(c);
      if (c.length > 0 && !selectedComplaintId) {
        setSelectedComplaintId(c[0].id);
      }
      setAuditLogs(a);
      setAgentExecutions(ex);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAdminData();
  }, []);

  const handleSimulateStatus = async () => {
    if (!selectedComplaintId) return;
    setLoading(true);
    try {
      const res = await adminSimulateStatus(selectedComplaintId, targetStatus, notes);
      setMsg(res.message);
      fetchAdminData();
    } catch (e: any) {
      alert(e.message || 'Simulation failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-bold text-white tracking-tight">Admin Demo Control Panel</h2>
            <span className="px-2.5 py-0.5 rounded text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">
              Simulation Controls
            </span>
          </div>
          <p className="text-xs text-gray-400">Section 21: Simulate SLA breaches, status progressions & review agent telemetry for judges</p>
        </div>
        <button
          onClick={fetchAdminData}
          className="px-3.5 py-2 rounded-xl glass-panel hover:bg-gray-800 text-xs text-gray-300 flex items-center gap-2"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          Refresh Logs
        </button>
      </div>

      {msg && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 shrink-0 text-emerald-400" />
          <span>{msg}</span>
        </div>
      )}

      {/* Demo Fast-Forward Simulation Panel */}
      <div className="glass-panel-glow rounded-2xl p-6 sm:p-8 border border-amber-500/30 space-y-6">
        <div className="flex items-center gap-3 border-b border-gray-800 pb-4">
          <div className="w-10 h-10 rounded-xl bg-amber-500/20 text-amber-400 border border-amber-500/30 flex items-center justify-center">
            <Play className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white">Simulate Complaint Status Progression</h3>
            <p className="text-xs text-gray-400">Allows hackathon judges to experience full lifecycle without waiting 72 real hours</p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div>
            <label className="block text-xs font-semibold text-gray-300 mb-1">Target Complaint</label>
            <select
              value={selectedComplaintId}
              onChange={(e) => setSelectedComplaintId(e.target.value)}
              className="w-full px-3.5 py-2.5 rounded-xl bg-gray-900 border border-gray-700 text-xs text-gray-200 focus:outline-none focus:border-amber-500"
            >
              {complaints.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.complaint_number} - {c.category} ({c.status})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-gray-300 mb-1">Fast-Forward Status To</label>
            <select
              value={targetStatus}
              onChange={(e) => setTargetStatus(e.target.value)}
              className="w-full px-3.5 py-2.5 rounded-xl bg-gray-900 border border-gray-700 text-xs text-gray-200 focus:outline-none focus:border-amber-500"
            >
              <option value="SUBMITTED">SUBMITTED</option>
              <option value="ACKNOWLEDGED">ACKNOWLEDGED</option>
              <option value="ASSIGNED">ASSIGNED</option>
              <option value="IN_PROGRESS">IN_PROGRESS</option>
              <option value="ESCALATED">ESCALATED (Simulate SLA Breach)</option>
              <option value="RESOLVED">RESOLVED</option>
              <option value="VERIFIED_RESOLVED">VERIFIED_RESOLVED</option>
            </select>
          </div>

          <div className="flex items-end">
            <button
              onClick={handleSimulateStatus}
              disabled={loading || !selectedComplaintId}
              className="w-full py-2.5 px-4 rounded-xl bg-amber-600 hover:bg-amber-500 text-white font-semibold text-xs shadow-lg shadow-amber-600/30 flex items-center justify-center gap-2"
            >
              <Play className="w-4 h-4" />
              Fast-Forward Status Now
            </button>
          </div>
        </div>
      </div>

      {/* Telemetry Grid: Agent Executions & Audit Logs */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Agent Telemetry */}
        <div className="glass-panel rounded-2xl p-6 border border-gray-800 space-y-4">
          <div className="flex items-center justify-between border-b border-gray-800 pb-3">
            <div className="flex items-center gap-2">
              <Cpu className="w-4 h-4 text-indigo-400" />
              <h3 className="text-sm font-bold text-white">Agent Execution Logs (Observability)</h3>
            </div>
            <span className="text-[10px] text-gray-500">Section 30 Telemetry</span>
          </div>

          <div className="space-y-3 max-h-96 overflow-y-auto pr-1">
            {agentExecutions.map((ex) => (
              <div key={ex.id} className="p-3 rounded-xl bg-gray-900/60 border border-gray-800 text-xs flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-mono font-bold text-indigo-300">{ex.agent_name}</span>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                      ex.status === 'SUCCESS' ? 'bg-emerald-500/20 text-emerald-300' : 'bg-amber-500/20 text-amber-300'
                    }`}>
                      {ex.status}
                    </span>
                  </div>
                  <span className="text-[10px] text-gray-500 block mt-1">
                    Latency: {ex.execution_time_ms}ms | Confidence: {(ex.confidence * 100).toFixed(0)}%
                  </span>
                </div>
                <span className="text-[10px] text-gray-600 font-mono">
                  {new Date(ex.created_at).toLocaleTimeString()}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* System Audit Logs */}
        <div className="glass-panel rounded-2xl p-6 border border-gray-800 space-y-4">
          <div className="flex items-center justify-between border-b border-gray-800 pb-3">
            <div className="flex items-center gap-2">
              <Activity className="w-4 h-4 text-teal-400" />
              <h3 className="text-sm font-bold text-white">Immutable Audit Trail</h3>
            </div>
            <span className="text-[10px] text-gray-500">Section 29 Audit Engine</span>
          </div>

          <div className="space-y-3 max-h-96 overflow-y-auto pr-1">
            {auditLogs.map((log) => (
              <div key={log.id} className="p-3 rounded-xl bg-gray-900/60 border border-gray-800 text-xs space-y-1">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-gray-200">{log.action}</span>
                  <span className="text-[10px] text-gray-500 font-mono">{new Date(log.created_at).toLocaleTimeString()}</span>
                </div>
                <div className="text-[11px] text-gray-400 flex items-center gap-2">
                  <span>Actor: {log.actor}</span>
                  <span>•</span>
                  <span>Entity: {log.entity_type} ({log.entity_id})</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
