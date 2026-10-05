import React from 'react';
import { AlertCircle, Shield, Map, FileText, Settings, Sparkles, CheckCircle2 } from 'lucide-react';

interface HeaderProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  onRunDemoScenario?: () => void;
}

export const Header: React.FC<HeaderProps> = ({ activeTab, setActiveTab, onRunDemoScenario }) => {
  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-gray-800">
      {/* Simulation Banner */}
      <div className="bg-amber-500/10 border-b border-amber-500/20 px-4 py-1.5 text-xs text-amber-300 flex items-center justify-center gap-2 font-medium">
        <AlertCircle className="w-3.5 h-3.5 text-amber-400" />
        <span>CivicFix Demo Civic API — Simulation Only</span>
        <span className="opacity-60">|</span>
        <span className="text-gray-400">All municipal calls operate against internal simulated gateway</span>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand Logo */}
        <div 
          onClick={() => setActiveTab('landing')}
          className="flex items-center gap-3 cursor-pointer group"
        >
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/20 group-hover:scale-105 transition-transform">
            <Shield className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-lg text-white tracking-tight">CivicFix</span>
              <span className="px-1.5 py-0.5 rounded text-[10px] font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">AI</span>
            </div>
            <p className="text-[10px] text-gray-400">Multi-Agent Civic Orchestration</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex items-center gap-1 bg-gray-900/60 p-1 rounded-xl border border-gray-800">
          <button
            onClick={() => setActiveTab('report')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-2 ${
              activeTab === 'report'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/50'
            }`}
          >
            <Sparkles className="w-3.5 h-3.5" />
            Report Issue
          </button>
          <button
            onClick={() => setActiveTab('tracking')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-2 ${
              activeTab === 'tracking' || activeTab === 'details'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/50'
            }`}
          >
            <FileText className="w-3.5 h-3.5" />
            Dashboard
          </button>
          <button
            onClick={() => setActiveTab('map')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-2 ${
              activeTab === 'map'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/50'
            }`}
          >
            <Map className="w-3.5 h-3.5" />
            Issue Map
          </button>
          <button
            onClick={() => setActiveTab('admin')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-2 ${
              activeTab === 'admin'
                ? 'bg-amber-600 text-white shadow-md shadow-amber-600/30'
                : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/50'
            }`}
          >
            <Settings className="w-3.5 h-3.5" />
            Admin Demo Panel
          </button>
        </nav>

        {/* Demo Quick Run Button */}
        {onRunDemoScenario && (
          <button
            onClick={onRunDemoScenario}
            className="hidden lg:flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-semibold bg-gradient-to-r from-emerald-600 to-teal-600 text-white hover:opacity-95 shadow-lg shadow-emerald-600/20 transition-all"
          >
            <CheckCircle2 className="w-3.5 h-3.5" />
            Run Demo Scenario
          </button>
        )}
      </div>
    </header>
  );
};
