const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

export async function createIssue(formData: FormData) {
  const response = await fetch(`${API_BASE_URL}/issues`, {
    method: 'POST',
    body: formData,
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to report issue');
  }
  return response.json();
}

export async function analyzeIssue(issueId: string) {
  const response = await fetch(`${API_BASE_URL}/issues/${issueId}/analyze`, {
    method: 'POST',
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to run AI analysis');
  }
  return response.json();
}

export async function approveComplaint(complaintId: string, payload: { approved: boolean; edited_body?: string; edited_requested_action?: string }) {
  const response = await fetch(`${API_BASE_URL}/complaints/${complaintId}/approve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to approve complaint');
  }
  return response.json();
}

export async function getComplaintDetails(complaintId: string) {
  const response = await fetch(`${API_BASE_URL}/complaints/${complaintId}`);
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to fetch complaint details');
  }
  return response.json();
}

export async function escalateComplaint(complaintId: string) {
  const response = await fetch(`${API_BASE_URL}/complaints/${complaintId}/escalate`, {
    method: 'POST',
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to escalate complaint');
  }
  return response.json();
}

export async function verifyResolution(complaintId: string, formData: FormData) {
  const response = await fetch(`${API_BASE_URL}/complaints/${complaintId}/verify`, {
    method: 'POST',
    body: formData,
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to verify resolution');
  }
  return response.json();
}

export async function getDashboardStats() {
  const response = await fetch(`${API_BASE_URL}/dashboard/stats`);
  if (!response.ok) throw new Error('Failed to fetch dashboard stats');
  return response.json();
}

export async function listComplaints() {
  const response = await fetch(`${API_BASE_URL}/dashboard/complaints`);
  if (!response.ok) throw new Error('Failed to fetch complaints list');
  return response.json();
}

export async function getMapIssues() {
  const response = await fetch(`${API_BASE_URL}/map/issues`);
  if (!response.ok) throw new Error('Failed to fetch map markers');
  return response.json();
}

export async function getAuditLogs() {
  const response = await fetch(`${API_BASE_URL}/admin/audit-logs`);
  if (!response.ok) throw new Error('Failed to fetch audit logs');
  return response.json();
}

export async function getAgentExecutions() {
  const response = await fetch(`${API_BASE_URL}/admin/agent-executions`);
  if (!response.ok) throw new Error('Failed to fetch agent executions');
  return response.json();
}

export async function adminSimulateStatus(complaintId: string, newStatus: string, notes?: string) {
  const response = await fetch(`${API_BASE_URL}/admin/simulate-status`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ complaint_id: complaintId, new_status: newStatus, notes }),
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to simulate status');
  }
  return response.json();
}
