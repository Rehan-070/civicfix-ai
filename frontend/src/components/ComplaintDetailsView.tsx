import React, { useEffect, useState, useRef } from 'react';
import { 
  ArrowLeft, Clock, AlertTriangle, ShieldCheck, Upload, CheckCircle2, 
  Building2, MapPin, FileText, ChevronRight, AlertCircle, Sparkles, Check
} from 'lucide-react';
import { getComplaintDetails, escalateComplaint, verifyResolution } from '../services/api';

interface ComplaintDetailsViewProps {
  complaintId: string;
  onBack: () => void;
}

export const ComplaintDetailsView: React.FC<ComplaintDetailsViewProps> = ({ complaintId, onBack }) => {
  const [details, setDetails] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Verification Upload State
  const [afterFile, setAfterFile] = useState<File | null>(null);
  const [afterPreview, setAfterPreview] = useState<string | null>(null);
  const [verifying, setVerifying] = useState(false);
  const [verificationResult, setVerificationResult] = useState<any>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const fetchDetails = async () => {
    setLoading(true);
    try {
      const data = await getComplaintDetails(complaintId);
      setDetails(data);
    } catch (e: any) {
      setErrorMsg(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDetails();
  }, [complaintId]);

  const handleEscalate = async () => {
    try {
      await escalateComplaint(complaintId);
      fetchDetails();
    } catch (e: any) {
      alert(e.message || 'Escalation failed');
    }
  };

  const handleAfterFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setAfterFile(file);
      setAfterPreview(URL.createObjectURL(file));
    }
  };

  const handleVerifySubmit = async () => {
    if (!afterFile) return;
    setVerifying(true);
    try {
      const formData = new FormData();
      formData.append('file', afterFile);
      const res = await verifyResolution(complaintId, formData);
      setVerificationResult(res);
      fetchDetails();
    } catch (e: any) {
      alert(e.message || 'Verification failed');
    } finally {
      setVerifying(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto p-12 text-center text-gray-400">
        Loading ticket details...
      </div>
    );
  }

  if (errorMsg || !details) {
    return (
      <div className="max-w-5xl mx-auto p-8 text-center text-rose-400">
        {errorMsg || 'Complaint details not found.'}
        <button onClick={onBack} className="block mt-4 mx-auto text-xs text-indigo-400 underline">
          Go Back to Dashboard
        </button>
      </div>
    );
  }

  const isEscalated = details.status === 'ESCALATED' || details.is_sla_breached;
  const isVerified = details.status === 'VERIFIED_RESOLVED';

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 space-y-8">
      {/* Back Header */}
      <button
        onClick={onBack}
        className="inline-flex items-center gap-2 text-xs font-semibold text-gray-400 hover:text-white transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to Dashboard
      </button>

      {/* SLA Breach Alert Notice */}
      {isEscalated && (
        <div className="p-5 rounded-2xl bg-rose-500/10 border border-rose-500/30 text-rose-300 flex items-start gap-4">
          <AlertTriangle className="w-6 h-6 shrink-0 text-rose-400 mt-1" />
          <div className="space-y-1">
            <span className="font-bold text-sm block">SLA Deadline Breached — Automatic Escalation Triggered</span>
            <p className="text-xs text-rose-200/80">
              The configured SLA of {details.sla_hours} hours was exceeded without field confirmation. Ticket status has been updated to ESCALATED and dispatched to the Senior Supervisor.
            </p>
          </div>
        </div>
      )}

      {/* Main Ticket Summary Box */}
      <div className="glass-panel rounded-2xl p-6 sm:p-8 border border-gray-800 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-gray-800 pb-6">
          <div>
            <div className="flex items-center gap-3">
              <span className="font-mono text-lg font-bold text-indigo-400">{details.complaint_number}</span>
              <span className="px-3 py-1 rounded-full text-xs font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                {details.status}
              </span>
            </div>
            <h1 className="text-xl font-extrabold text-white mt-1">{details.category} Issue Report</h1>
          </div>

          {!isEscalated && !isVerified && (
            <button
              onClick={handleEscalate}
              className="px-4 py-2 rounded-xl text-xs font-semibold bg-rose-600/20 hover:bg-rose-600/30 text-rose-300 border border-rose-500/30 transition-colors"
            >
              Simulate SLA Breach & Escalate
            </button>
          )}
        </div>

        {/* Info Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="p-4 rounded-xl bg-gray-900/60 border border-gray-800">
            <span className="text-[10px] uppercase tracking-wider text-gray-500 block">Department</span>
            <span className="text-xs font-semibold text-gray-200 flex items-center gap-1.5 mt-1">
              <Building2 className="w-3.5 h-3.5 text-indigo-400" />
              {details.department_name}
            </span>
          </div>

          <div className="p-4 rounded-xl bg-gray-900/60 border border-gray-800">
            <span className="text-[10px] uppercase tracking-wider text-gray-500 block">Jurisdiction</span>
            <span className="text-xs font-semibold text-gray-200 flex items-center gap-1.5 mt-1">
              <MapPin className="w-3.5 h-3.5 text-indigo-400" />
              {details.ward}
            </span>
          </div>

          <div className="p-4 rounded-xl bg-gray-900/60 border border-gray-800">
            <span className="text-[10px] uppercase tracking-wider text-gray-500 block">SLA Target</span>
            <span className="text-xs font-semibold text-amber-400 flex items-center gap-1.5 mt-1">
              <Clock className="w-3.5 h-3.5" />
              {details.sla_hours} Hours
            </span>
          </div>

          <div className="p-4 rounded-xl bg-gray-900/60 border border-gray-800">
            <span className="text-[10px] uppercase tracking-wider text-gray-500 block">Severity</span>
            <span className="text-xs font-semibold text-rose-400 block mt-1">
              {details.severity}
            </span>
          </div>
        </div>

        {/* Body & Requested Action */}
        <div className="space-y-4 pt-2">
          <div>
            <span className="text-xs font-semibold text-gray-400 block mb-1">Official Complaint Document Body</span>
            <div className="p-4 rounded-xl bg-gray-900/80 border border-gray-800 text-xs text-gray-300 font-mono leading-relaxed">
              {details.formatted_body}
            </div>
          </div>

          <div>
            <span className="text-xs font-semibold text-gray-400 block mb-1">Requested Remedial Action</span>
            <div className="p-3 rounded-xl bg-gray-900/80 border border-gray-800 text-xs text-gray-300 font-mono">
              {details.requested_action}
            </div>
          </div>
        </div>
      </div>

      {/* Resolution Verification Panel (Section 4 Rule 8) */}
      <div className="glass-panel-glow rounded-2xl p-6 sm:p-8 border border-indigo-500/30 space-y-6">
        <div className="flex items-center gap-3 border-b border-gray-800 pb-4">
          <div className="w-10 h-10 rounded-xl bg-teal-500/20 text-teal-400 border border-teal-500/30 flex items-center justify-center">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white">AI-Assisted Resolution Verification</h3>
            <p className="text-xs text-gray-400">Rule 8 Enforced: Confidence-based verification of before/after resolution evidence</p>
          </div>
        </div>

        {details.verifications && details.verifications.length > 0 ? (
          <div className="p-5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4" />
                Result: {details.verifications[0].result}
              </span>
              <span className="text-xs font-semibold text-emerald-300">
                Confidence: {(details.verifications[0].confidence * 100).toFixed(0)}%
              </span>
            </div>
            <div className="text-xs text-gray-300 font-mono leading-relaxed whitespace-pre-line">
              {details.verifications[0].summary}
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <span className="text-xs text-gray-300 block">
              Submit resolution evidence photo (e.g. repaired road/pothole after repair) to trigger the Verification Agent.
            </span>

            <div
              onClick={() => fileInputRef.current?.click()}
              className="border-2 border-dashed border-gray-700 hover:border-teal-500/50 rounded-xl p-6 text-center cursor-pointer bg-gray-900/40"
            >
              <input
                ref={fileInputRef}
                type="file"
                accept="image/jpeg,image/png,image/webp"
                onChange={handleAfterFileChange}
                className="hidden"
              />

              {afterPreview ? (
                <div className="inline-block">
                  <img src={afterPreview} alt="After Evidence" className="max-h-48 rounded-lg shadow-lg" />
                  <span className="block mt-2 text-xs text-teal-300">Click to change after-photo</span>
                </div>
              ) : (
                <div className="flex flex-col items-center">
                  <Upload className="w-6 h-6 text-gray-500 mb-2" />
                  <span className="text-xs font-semibold text-gray-300">Upload "After" Resolution Evidence Photo</span>
                </div>
              )}
            </div>

            {afterFile && (
              <button
                onClick={handleVerifySubmit}
                disabled={verifying}
                className="w-full py-3 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-semibold text-xs shadow-lg shadow-teal-600/30 flex items-center justify-center gap-2"
              >
                <Sparkles className="w-4 h-4" />
                {verifying ? 'Running Verification Agent...' : 'Run AI Resolution Verification Agent'}
              </button>
            )}
          </div>
        )}
      </div>

      {/* Timeline Section */}
      <div className="glass-panel rounded-2xl p-6 sm:p-8 border border-gray-800">
        <h3 className="text-base font-bold text-white mb-6">Complaint Lifecycle Timeline</h3>

        <div className="space-y-6 relative before:absolute before:inset-0 before:left-3.5 before:w-0.5 before:bg-gray-800">
          {details.timeline && details.timeline.map((item: any, idx: number) => (
            <div key={idx} className="relative flex items-start gap-4 pl-8">
              <div className="absolute left-1.5 top-1 w-4 h-4 rounded-full bg-indigo-600 border-2 border-gray-900" />
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-white">{item.status}</span>
                  <span className="text-[10px] text-gray-500">by {item.changed_by}</span>
                </div>
                <p className="text-xs text-gray-400 mt-1">{item.notes}</p>
                <span className="text-[10px] text-gray-600 mt-1 block">
                  {new Date(item.timestamp).toLocaleString()}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
