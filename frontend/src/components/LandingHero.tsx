import React from 'react';
import { Camera, Cpu, Building2, Send, Clock, CheckCircle, ArrowRight, ShieldCheck } from 'lucide-react';

interface LandingHeroProps {
  onStartReport: () => void;
  onViewDemo: () => void;
}

export const LandingHero: React.FC<LandingHeroProps> = ({ onStartReport, onViewDemo }) => {
  return (
    <div className="relative overflow-hidden py-16 sm:py-24">
      {/* Subtle Background Glows */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-96 h-96 bg-indigo-600/15 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute top-1/3 left-1/3 w-64 h-64 bg-purple-600/10 rounded-full blur-3xl pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-medium mb-6">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>AI-Assisted Civic Resolution Workflow</span>
        </div>

        {/* Hero Headings */}
        <h1 className="text-4xl sm:text-6xl font-extrabold text-white tracking-tight leading-tight max-w-4xl mx-auto">
          See it. Report it. <br />
          <span className="bg-gradient-to-r from-indigo-400 via-purple-300 to-emerald-400 bg-clip-text text-transparent">
            Get it Fixed.
          </span>
        </h1>

        <p className="mt-6 text-lg sm:text-xl text-gray-300 max-w-2xl mx-auto font-light leading-relaxed">
          AI-powered civic issue reporting, tracking, escalation, and resolution verification. Turn visible problems into structured, trackable civic workflows.
        </p>

        {/* CTA Buttons */}
        <div className="mt-10 flex flex-wrap justify-center gap-4">
          <button
            onClick={onStartReport}
            className="px-6 py-3.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm shadow-xl shadow-indigo-600/30 flex items-center gap-2 transition-all hover:scale-105"
          >
            <Camera className="w-4 h-4" />
            Report a Civic Issue
          </button>
          <button
            onClick={onViewDemo}
            className="px-6 py-3.5 rounded-xl glass-panel hover:bg-gray-800/80 text-gray-200 font-semibold text-sm border border-gray-700 flex items-center gap-2 transition-all"
          >
            View Demo Scenario
            <ArrowRight className="w-4 h-4 text-gray-400" />
          </button>
        </div>

        {/* Workflow Lifecycle Diagram */}
        <div className="mt-20 glass-panel rounded-2xl p-6 sm:p-8 max-w-5xl mx-auto border border-gray-800">
          <div className="text-xs uppercase tracking-wider font-semibold text-indigo-400 mb-8">
            End-to-End Orchestrated Civic Lifecycle
          </div>

          <div className="grid grid-cols-2 md:grid-cols-6 gap-4 relative">
            {/* Step 1 */}
            <div className="flex flex-col items-center p-3 rounded-xl bg-gray-900/40 border border-gray-800">
              <div className="w-10 h-10 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center mb-3">
                <Camera className="w-5 h-5" />
              </div>
              <span className="text-xs font-semibold text-white">1. Citizen Photo</span>
              <span className="text-[10px] text-gray-400 mt-1">Upload Pothole / Issue</span>
            </div>

            {/* Step 2 */}
            <div className="flex flex-col items-center p-3 rounded-xl bg-gray-900/40 border border-gray-800">
              <div className="w-10 h-10 rounded-lg bg-purple-500/20 text-purple-400 flex items-center justify-center mb-3">
                <Cpu className="w-5 h-5" />
              </div>
              <span className="text-xs font-semibold text-white">2. AI Vision Perception</span>
              <span className="text-[10px] text-gray-400 mt-1">Classify & Severity</span>
            </div>

            {/* Step 3 */}
            <div className="flex flex-col items-center p-3 rounded-xl bg-gray-900/40 border border-gray-800">
              <div className="w-10 h-10 rounded-lg bg-blue-500/20 text-blue-400 flex items-center justify-center mb-3">
                <Building2 className="w-5 h-5" />
              </div>
              <span className="text-xs font-semibold text-white">3. Authority Mapping</span>
              <span className="text-[10px] text-gray-400 mt-1">Rule DB Department</span>
            </div>

            {/* Step 4 */}
            <div className="flex flex-col items-center p-3 rounded-xl bg-gray-900/40 border border-gray-800">
              <div className="w-10 h-10 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center mb-3">
                <Send className="w-5 h-5" />
              </div>
              <span className="text-xs font-semibold text-white">4. Human Approval</span>
              <span className="text-[10px] text-gray-400 mt-1">Submit to Demo Gateway</span>
            </div>

            {/* Step 5 */}
            <div className="flex flex-col items-center p-3 rounded-xl bg-gray-900/40 border border-gray-800">
              <div className="w-10 h-10 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center mb-3">
                <Clock className="w-5 h-5" />
              </div>
              <span className="text-xs font-semibold text-white">5. SLA Tracking</span>
              <span className="text-[10px] text-gray-400 mt-1">Deterministic Timer</span>
            </div>

            {/* Step 6 */}
            <div className="flex flex-col items-center p-3 rounded-xl bg-gray-900/40 border border-gray-800">
              <div className="w-10 h-10 rounded-lg bg-teal-500/20 text-teal-400 flex items-center justify-center mb-3">
                <CheckCircle className="w-5 h-5" />
              </div>
              <span className="text-xs font-semibold text-white">6. AI Verification</span>
              <span className="text-[10px] text-gray-400 mt-1">Before / After Check</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
