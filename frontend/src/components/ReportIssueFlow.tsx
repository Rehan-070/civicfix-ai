import React, { useState, useRef } from 'react';
import { Upload, MapPin, Sparkles, AlertTriangle, CheckCircle, Loader2, ArrowRight } from 'lucide-react';
import { createIssue, analyzeIssue } from '../services/api';

interface ReportIssueFlowProps {
  onAnalysisCompleted: (analysisResult: any) => void;
}

export const ReportIssueFlow: React.FC<ReportIssueFlowProps> = ({ onAnalysisCompleted }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [address, setAddress] = useState('4th Cross Road, Demo Ward 04');
  const [ward, setWard] = useState('Demo Ward 04');
  const [lat, setLat] = useState<number>(12.9716);
  const [lon, setLon] = useState<number>(77.5946);

  const [loading, setLoading] = useState(false);
  const [analysisState, setAnalysisState] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setErrorMsg(null);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setErrorMsg(null);
    }
  };

  const handleUseLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          setLat(pos.coords.latitude);
          setLon(pos.coords.longitude);
          setAddress(`GPS Location (${pos.coords.latitude.toFixed(4)}, ${pos.coords.longitude.toFixed(4)}), Demo Ward 04`);
        },
        () => {
          setErrorMsg('Could not fetch GPS. Using default Demo Ward location.');
        }
      );
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) {
      setErrorMsg('Please select or upload a civic issue photo first.');
      return;
    }

    setLoading(true);
    setErrorMsg(null);
    setAnalysisState('Uploading evidence & registering issue...');

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('latitude', lat.toString());
      formData.append('longitude', lon.toString());
      formData.append('address', address);
      formData.append('ward', ward);

      // 1. Create Issue record
      const issueRes = await createIssue(formData);

      // 2. Run AI Analysis Pipeline
      setAnalysisState('Executing Vision, Location, Authority & Complaint Agents...');
      const analysisRes = await analyzeIssue(issueRes.issue_id);

      setLoading(false);
      setAnalysisState(null);

      // Pass result to parent to trigger Complaint Preview Modal
      onAnalysisCompleted(analysisRes);

    } catch (err: any) {
      setLoading(false);
      setAnalysisState(null);
      setErrorMsg(err.message || 'An error occurred during issue processing.');
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <div className="glass-panel rounded-2xl p-6 sm:p-8 border border-gray-800">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white">Report a Visible Civic Problem</h2>
            <p className="text-xs text-gray-400">AI perception will detect issue category, severity & responsible authority</p>
          </div>
        </div>

        {errorMsg && (
          <div className="mb-6 p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 shrink-0" />
            <span>{errorMsg}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* File Upload Zone */}
          <div>
            <label className="block text-xs font-semibold text-gray-300 mb-2">
              1. Issue Photo Evidence
            </label>
            <div
              onDragOver={handleDragOver}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className={`border-2 border-dashed rounded-2xl p-6 text-center cursor-pointer transition-all ${
                previewUrl
                  ? 'border-indigo-500/50 bg-gray-900/60'
                  : 'border-gray-700 hover:border-indigo-500/50 bg-gray-900/30 hover:bg-gray-900/50'
              }`}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept="image/jpeg,image/png,image/webp"
                onChange={handleFileChange}
                className="hidden"
              />

              {previewUrl ? (
                <div className="relative inline-block group">
                  <img
                    src={previewUrl}
                    alt="Civic Issue Preview"
                    className="max-h-64 rounded-xl object-cover shadow-lg border border-gray-700"
                  />
                  <div className="mt-3 text-xs text-indigo-300 font-medium">
                    Click or drag to change image
                  </div>
                </div>
              ) : (
                <div className="py-6 flex flex-col items-center">
                  <div className="w-12 h-12 rounded-full bg-gray-800 flex items-center justify-center mb-3 text-gray-400 group-hover:text-indigo-400">
                    <Upload className="w-6 h-6" />
                  </div>
                  <span className="text-sm font-semibold text-gray-200">
                    Upload Photo of Pothole, Garbage, Streetlight...
                  </span>
                  <span className="text-xs text-gray-500 mt-1">
                    Drag and drop or click to browse (JPEG, PNG, WebP)
                  </span>
                </div>
              )}
            </div>
          </div>

          {/* Location Picker */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="text-xs font-semibold text-gray-300">
                2. Location & Jurisdiction
              </label>
              <button
                type="button"
                onClick={handleUseLocation}
                className="text-xs text-indigo-400 hover:text-indigo-300 flex items-center gap-1 font-medium"
              >
                <MapPin className="w-3.5 h-3.5" />
                Use GPS Coordinates
              </button>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <input
                  type="text"
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  placeholder="Street address or landmark"
                  className="w-full px-4 py-2.5 rounded-xl bg-gray-900/80 border border-gray-700 text-gray-200 text-sm focus:outline-none focus:border-indigo-500"
                />
              </div>
              <div>
                <select
                  value={ward}
                  onChange={(e) => setWard(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl bg-gray-900/80 border border-gray-700 text-gray-200 text-sm focus:outline-none focus:border-indigo-500"
                >
                  <option value="Demo Ward 04">Demo Ward 04 (Central District)</option>
                  <option value="Demo Ward 01">Demo Ward 01 (North Zone)</option>
                  <option value="Demo Ward 02">Demo Ward 02 (East Zone)</option>
                  <option value="Demo Ward 03">Demo Ward 03 (West Zone)</option>
                </select>
              </div>
            </div>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading || !selectedFile}
            className={`w-full py-3.5 px-6 rounded-xl text-sm font-semibold shadow-xl flex items-center justify-center gap-2 transition-all ${
              loading || !selectedFile
                ? 'bg-gray-800 text-gray-500 cursor-not-allowed'
                : 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-indigo-600/30 hover:scale-[1.01]'
            }`}
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin text-indigo-300" />
                <span>{analysisState || 'Analyzing...'}</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>Run AI Issue Perception Pipeline</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
};
