/**
 * API service for communicating with backend
 */
import axios from 'axios';
import type {
  UploadResponse,
  AnalysisRequest,
  ResumeAnalysisResult,
} from '../types/analysis';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Upload a resume file
 */
export const uploadResume = async (file: File): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post<UploadResponse>('/upload/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

/**
 * Delete an uploaded file
 */
export const deleteFile = async (fileId: string): Promise<void> => {
  await api.delete(`/upload/${fileId}`);
};

/**
 * Analyze a resume
 */
export const analyzeResume = async (
  request: AnalysisRequest
): Promise<ResumeAnalysisResult> => {
  const response = await api.post<ResumeAnalysisResult>(
    '/analyze/',
    request
  );

  return response.data;
};

/**
 * Quick analysis (key metrics only)
 */
export const quickAnalyze = async (request: AnalysisRequest): Promise<any> => {
  const response = await api.post('/analyze/quick', request);
  return response.data;
};

/**
 * Health check
 */
export const healthCheck = async (): Promise<any> => {
  const response = await api.get('/health');
  return response.data;
};

/**
 * Analyzer health check
 */
export const analyzerHealth = async (): Promise<any> => {
  const response = await api.get('/analyze/health');
  return response.data;
};

export default api;
