import React, { useState } from 'react';
import { Header } from './components/Header';
import { LandingHero } from './components/LandingHero';
import { ReportIssueFlow } from './components/ReportIssueFlow';
import { ComplaintPreviewModal } from './components/ComplaintPreviewModal';
import { TrackingDashboard } from './components/TrackingDashboard';
import { ComplaintDetailsView } from './components/ComplaintDetailsView';
import { MapView } from './components/MapView';
import { AdminControlPanel } from './components/AdminControlPanel';
import { approveComplaint, createIssue, analyzeIssue, escalateComplaint, verifyResolution } from './services/api';

export function App() {
  const [activeTab, setActiveTab] = useState<string>('landing');
  const [analysisResult, setAnalysisResult] = useState<any | null>(null);
  const [selectedComplaintId, setSelectedComplaintId] = useState<string | null>(null);

  // Quick Hackathon Demo Scenario Runner
  const handleRunDemoScenario = async () => {
    try {
      setActiveTab('report');
      // Create sample pothole image blob
      const canvas = document.createElement('canvas');
      canvas.width = 400;
      canvas.height = 300;
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.fillStyle = '#374151';
        ctx.fillRect(0, 0, 400, 300);
        ctx.fillStyle = '#111827';
        ctx.beginPath();
        ctx.arc(200, 150, 60, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#f59e0b';
        ctx.font = '14px sans-serif';
        ctx.fillText('DEMO POTHOLE EVIDENCE', 110, 290);
      }

      canvas.toBlob(async (blob) => {
        if (!blob) return;
        const file = new File([blob], 'demo_pothole.png', { type: 'image/png' });
        const formData = new FormData();
        formData.append('file', file);
        formData.append('latitude', '12.9716');
        formData.append('longitude', '77.5946');
        formData.append('address', '4th Cross Road, Demo Ward 04');
        formData.append('ward', 'Demo Ward 04');

        const issueRes = await createIssue(formData);
        const analysisRes = await analyzeIssue(issueRes.issue_id);
        setAnalysisResult(analysisRes);
      }, 'image/png');
    } catch (e: any) {
      alert(`Demo Scenario error: ${e.message}`);
    }
  };

  const handleAnalysisCompleted = (res: any) => {
    setAnalysisResult(res);
  };

  const handleApproveComplaint = async (payload: { approved: boolean; edited_body?: string; edited_requested_action?: string }) => {
    if (!analysisResult || !analysisResult.complaint) return;
    try {
      const complaintId = analysisResult.complaint.id;
      await approveComplaint(complaintId, payload);
      setAnalysisResult(null);
      setSelectedComplaintId(complaintId);
      setActiveTab('details');
    } catch (e: any) {
      alert(e.message || 'Approval failed');
    }
  };

  const handleSelectComplaint = (complaintId: string) => {
    setSelectedComplaintId(complaintId);
    setActiveTab('details');
  };

  return (
    <div className="min-h-screen bg-[#0b0f19] text-gray-100 font-sans selection:bg-indigo-500 selection:text-white">
      {/* Navbar with Demo simulation banner */}
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onRunDemoScenario={handleRunDemoScenario}
      />

      {/* Main Content Area */}
      <main className="pb-16">
        {activeTab === 'landing' && (
          <LandingHero
            onStartReport={() => setActiveTab('report')}
            onViewDemo={handleRunDemoScenario}
          />
        )}

        {activeTab === 'report' && (
          <ReportIssueFlow onAnalysisCompleted={handleAnalysisCompleted} />
        )}

        {activeTab === 'tracking' && (
          <TrackingDashboard onSelectComplaint={handleSelectComplaint} />
        )}

        {activeTab === 'details' && selectedComplaintId && (
          <ComplaintDetailsView
            complaintId={selectedComplaintId}
            onBack={() => setActiveTab('tracking')}
          />
        )}

        {activeTab === 'map' && (
          <MapView onSelectComplaint={handleSelectComplaint} />
        )}

        {activeTab === 'admin' && (
          <AdminControlPanel />
        )}
      </main>

      {/* Human Approval Preview Modal */}
      {analysisResult && (
        <ComplaintPreviewModal
          analysisResult={analysisResult}
          onApprove={handleApproveComplaint}
          onCancel={() => setAnalysisResult(null)}
        />
      )}
    </div>
  );
}

export default App;
