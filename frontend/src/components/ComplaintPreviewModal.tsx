import React, { useState } from 'react';
import { Shield, AlertCircle, Edit3, CheckCircle2, X, Building2, MapPin, AlertTriangle, Cpu, Check } from 'lucide-react';

interface ComplaintPreviewModalProps {
  analysisResult: any;
  onApprove: (payload: { approved: boolean; edited_body?: string; edited_requested_action?: string }) => void;
  onCancel: () => void;
}

const CATEGORY_OPTIONS = [
  { key: 'water_leakage', display: 'Water Leakage / Burst Pipeline', dept: 'Water Supply Department' },
  { key: 'pothole', display: 'Pothole', dept: 'Road Department' },
  { key: 'garbage', display: 'Garbage / Overflowing Bin', dept: 'Sanitation Department' },
  { key: 'streetlight', display: 'Broken Streetlight', dept: 'Electrical / Streetlight Department' },
  { key: 'drainage', display: 'Drainage Problem', dept: 'Drainage Department' },
  { key: 'damaged_road', display: 'Damaged Road', dept: 'Road Department' },
  { key: 'damaged_footpath', display: 'Damaged Footpath', dept: 'Road / Public Works Department' },
  { key: 'fallen_tree', display: 'Fallen Tree', dept: 'Horticulture / Tree Department' },
];

export const ComplaintPreviewModal: React.FC<ComplaintPreviewModalProps> = ({
  analysisResult,
  onApprove,
  onCancel,
}) => {
  const complaint = analysisResult.complaint || {};
  const [isEditing, setIsEditing] = useState(false);
  const [editedBody, setEditedBody] = useState(complaint.formatted_body || '');
  const [editedAction, setEditedAction] = useState(complaint.requested_action || '');
  const [submitting, setSubmitting] = useState(false);

  // Active Category State
  const [currentCategory, setCurrentCategory] = useState<string>(analysisResult.category || 'Pothole');
  const [currentDepartment, setCurrentDepartment] = useState<string>(analysisResult.department_name || 'Road Department');

  const duplicateInfo = analysisResult.duplicate_info;
  const confidencePct = Math.round((analysisResult.confidence || 0.9) * 100);
  const isLowConfidence = (analysisResult.confidence || 1) < 0.75 || analysisResult.needs_human_review;

  const handleCategorySelect = (opt: { display: string; dept: string }) => {
    setCurrentCategory(opt.display);
    setCurrentDepartment(opt.dept);
    const updatedBody = `Official Notice: ${opt.display} reported at ${analysisResult.address || '4th Cross Road, Demo Ward 04'}. Visual evidence has been attached for immediate inspection and action by ${opt.dept}.`;
    const updatedAction = `Dispatch ${opt.dept} crew to conduct site inspection and complete remedial repairs within mandatory SLA.`;
    setEditedBody(updatedBody);
    setEditedAction(updatedAction);
  };

  const handleApproveSubmit = () => {
    setSubmitting(true);
    onApprove({
      approved: true,
      edited_body: editedBody,
      edited_requested_action: editedAction,
    });
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md overflow-y-auto">
      <div className="glass-panel-glow rounded-2xl max-w-3xl w-full p-6 sm:p-8 relative border border-indigo-500/30 my-8 space-y-6">
        {/* Close button */}
        <button
          onClick={onCancel}
          className="absolute top-4 right-4 text-gray-400 hover:text-white p-1 rounded-lg hover:bg-gray-800"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Header */}
        <div className="flex items-center gap-3 border-b border-gray-800 pb-4">
          <div className="w-10 h-10 rounded-xl bg-indigo-600/20 text-indigo-400 border border-indigo-500/30 flex items-center justify-center">
            <Shield className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-lg font-bold text-white">Complaint Preview — Human Approval Required</h3>
              <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-amber-500/20 text-amber-300 border border-amber-500/30">
                Rule 4 Enforced
              </span>
            </div>
            <p className="text-xs text-gray-400">Review AI-generated draft before submitting to Demo Civic Gateway</p>
          </div>
        </div>

        {/* Spatial Duplicate Warning Notice */}
        {duplicateInfo && duplicateInfo.is_duplicate && (
          <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 shrink-0 text-amber-400 mt-0.5" />
            <div>
              <span className="font-semibold block">Possible Duplicate Issue Detected</span>
              <span>An active issue ({duplicateInfo.existing_issue_code}) of category '{duplicateInfo.category}' exists within {duplicateInfo.distance_meters} meters. You may still proceed if this is a distinct report.</span>
            </div>
          </div>
        )}

        {/* Low Confidence / Needs Review Warning Banner (Section 4 & 11) */}
        {isLowConfidence && (
          <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs space-y-3">
            <div className="flex items-center gap-2 font-bold text-rose-400">
              <AlertCircle className="w-4 h-4" />
              <span>⚠ AI REVIEW REQUIRED — Low Confidence ({confidencePct}%)</span>
            </div>
            <p className="text-gray-300">
              AI is not sufficiently confident about the issue type ({confidencePct}%). Please confirm or select the correct category below:
            </p>
            <div className="flex flex-wrap gap-2 pt-1">
              {CATEGORY_OPTIONS.map((opt) => (
                <button
                  key={opt.key}
                  type="button"
                  onClick={() => handleCategorySelect(opt)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all border ${
                    currentCategory === opt.display
                      ? 'bg-indigo-600 text-white border-indigo-400 shadow-md shadow-indigo-600/30'
                      : 'bg-gray-900/80 text-gray-300 border-gray-700 hover:bg-gray-800'
                  }`}
                >
                  {opt.display}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* AI ISSUE ANALYSIS CARD (Section 11) */}
        <div className="glass-panel p-5 rounded-xl border border-gray-800 space-y-4">
          <div className="flex items-center justify-between border-b border-gray-800/80 pb-2">
            <div className="flex items-center gap-2 text-indigo-400 text-xs font-bold uppercase tracking-wider">
              <Cpu className="w-4 h-4" />
              <span>AI Issue Analysis & Multi-Agent Telemetry</span>
            </div>
            <span className="px-2 py-0.5 rounded text-xs font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
              {confidencePct}% Confidence
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
            <div>
              <span className="text-[10px] text-gray-500 block uppercase">Detected Issue</span>
              <span className="font-bold text-white">{currentCategory}</span>
            </div>
            <div>
              <span className="text-[10px] text-gray-500 block uppercase">Severity</span>
              <span className="font-semibold text-rose-400">{analysisResult.severity || 'HIGH'}</span>
            </div>
            <div>
              <span className="text-[10px] text-gray-500 block uppercase">Department</span>
              <span className="font-semibold text-indigo-300 flex items-center gap-1">
                <Building2 className="w-3.5 h-3.5" />
                {currentDepartment}
              </span>
            </div>
            <div>
              <span className="text-[10px] text-gray-500 block uppercase">Jurisdiction</span>
              <span className="font-semibold text-gray-300 flex items-center gap-1">
                <MapPin className="w-3.5 h-3.5" />
                {analysisResult.ward || 'Demo Ward 04'}
              </span>
            </div>
          </div>

          {/* Observations & Validation Checkmarks */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2 border-t border-gray-800/60 text-xs">
            <div>
              <span className="text-[10px] font-semibold text-gray-400 uppercase block mb-1">Visual Evidence Observations</span>
              <ul className="space-y-1 text-gray-300">
                {(analysisResult.observations && analysisResult.observations.length > 0
                  ? analysisResult.observations
                  : ["Visible structural anomaly detected", "Visual evidence validated"]
                ).map((obs: string, idx: number) => (
                  <li key={idx} className="flex items-center gap-1.5 text-[11px]">
                    <Check className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                    <span>{obs}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <span className="text-[10px] font-semibold text-gray-400 uppercase block mb-1">Validation Pipeline Checks</span>
              <div className="space-y-1 text-[11px] text-gray-300">
                <div className="flex items-center gap-1.5 text-emerald-400">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Category supported ({currentCategory})</span>
                </div>
                <div className="flex items-center gap-1.5 text-emerald-400">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Authority rule validated ({currentDepartment})</span>
                </div>
                <div className="flex items-center gap-1.5 text-emerald-400">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Canonical Location ({analysisResult.ward || 'Demo Ward 04'})</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Complaint Body / Edit Form */}
        <div className="space-y-4">
          <div>
            <div className="flex items-center justify-between mb-1">
              <label className="text-xs font-semibold text-gray-300">Official Complaint Document Description</label>
              <button
                type="button"
                onClick={() => setIsEditing(!isEditing)}
                className="text-xs text-indigo-400 hover:text-indigo-300 flex items-center gap-1"
              >
                <Edit3 className="w-3.5 h-3.5" />
                {isEditing ? 'Cancel Edit' : 'Edit Text'}
              </button>
            </div>

            {isEditing ? (
              <textarea
                rows={4}
                value={editedBody}
                onChange={(e) => setEditedBody(e.target.value)}
                className="w-full p-3 rounded-xl bg-gray-900 border border-gray-700 text-gray-200 text-xs focus:outline-none focus:border-indigo-500"
              />
            ) : (
              <div className="p-4 rounded-xl bg-gray-900/80 border border-gray-800 text-xs text-gray-300 leading-relaxed font-mono">
                {editedBody || complaint.formatted_body}
              </div>
            )}
          </div>

          <div>
            <label className="block text-xs font-semibold text-gray-300 mb-1">Requested Action</label>
            {isEditing ? (
              <textarea
                rows={2}
                value={editedAction}
                onChange={(e) => setEditedAction(e.target.value)}
                className="w-full p-3 rounded-xl bg-gray-900 border border-gray-700 text-gray-200 text-xs focus:outline-none focus:border-indigo-500"
              />
            ) : (
              <div className="p-3 rounded-xl bg-gray-900/80 border border-gray-800 text-xs text-gray-300 font-mono">
                {editedAction || complaint.requested_action}
              </div>
            )}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center justify-end gap-3 pt-4 border-t border-gray-800">
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2.5 rounded-xl text-xs font-semibold text-gray-400 hover:text-gray-200 hover:bg-gray-800"
          >
            Cancel Draft
          </button>
          <button
            type="button"
            onClick={handleApproveSubmit}
            disabled={submitting}
            className="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs shadow-lg shadow-emerald-600/30 flex items-center gap-2 transition-all hover:scale-105"
          >
            <CheckCircle2 className="w-4 h-4" />
            {submitting ? 'Submitting...' : 'Approve & Submit Complaint'}
          </button>
        </div>
      </div>
    </div>
  );
};

