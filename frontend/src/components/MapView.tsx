import React, { useEffect, useState } from 'react';
import { MapPin, Building2, AlertTriangle, Shield, Eye } from 'lucide-react';
import { getMapIssues } from '../services/api';

interface MapViewProps {
  onSelectComplaint: (complaintId: string) => void;
}

export const MapView: React.FC<MapViewProps> = ({ onSelectComplaint }) => {
  const [markers, setMarkers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMapIssues()
      .then(setMarkers)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Interactive Civic Issue Map</h2>
          <p className="text-xs text-gray-400">Section 22: Geolocation markers for active municipal complaints</p>
        </div>
        <div className="flex items-center gap-2 text-xs text-amber-300 bg-amber-500/10 border border-amber-500/20 px-3 py-1.5 rounded-xl">
          <Shield className="w-3.5 h-3.5 text-amber-400" />
          <span>Location Privacy Protected — Fuzzified Grid</span>
        </div>
      </div>

      {loading ? (
        <div className="glass-panel p-12 text-center text-gray-400 rounded-2xl">
          Loading issue markers...
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {markers.map((m) => (
            <div
              key={m.id}
              onClick={() => onSelectComplaint(m.id)}
              className="glass-card rounded-2xl p-5 cursor-pointer flex flex-col justify-between border border-gray-800 hover:border-indigo-500/40"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="font-mono text-xs font-bold text-indigo-400">{m.issue_code}</span>
                  <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                    {m.status}
                  </span>
                </div>

                <div className="flex items-start gap-3 mb-3">
                  {m.image_url ? (
                    <img src={`http://127.0.0.1:8000${m.image_url}`} alt="Issue thumbnail" className="w-16 h-16 rounded-xl object-cover shrink-0 border border-gray-700" />
                  ) : (
                    <div className="w-16 h-16 rounded-xl bg-gray-800 flex items-center justify-center shrink-0 text-gray-600">
                      <MapPin className="w-6 h-6" />
                    </div>
                  )}
                  <div>
                    <h4 className="text-sm font-bold text-white">{m.category}</h4>
                    <span className="text-xs text-gray-400 flex items-center gap-1 mt-1">
                      <Building2 className="w-3 h-3 text-gray-500" />
                      {m.department_name}
                    </span>
                    <span className="text-[11px] text-gray-500 flex items-center gap-1 mt-0.5">
                      <MapPin className="w-3 h-3 text-gray-500" />
                      {m.latitude?.toFixed(4)}, {m.longitude?.toFixed(4)} ({m.ward})
                    </span>
                  </div>
                </div>
              </div>

              <div className="pt-3 border-t border-gray-800 flex items-center justify-between text-xs text-indigo-400 font-medium">
                <span>View Full Details</span>
                <Eye className="w-3.5 h-3.5" />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
