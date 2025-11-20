import { useState } from 'react';
import { Toaster, toast } from 'react-hot-toast';
import {
  DocumentTextIcon,
  SparklesIcon,
  ArrowPathIcon,
} from '@heroicons/react/24/outline';
import FileUpload from './components/FileUpload';
import ResultsDashboard from './components/ResultsDashboard';
import { uploadResume, analyzeResume } from './services/api';
import type { ResumeAnalysisResult } from './types/analysis';

type AnalysisStep = 'upload' | 'configure' | 'analyzing' | 'results';

function App() {
  const [step, setStep] = useState<AnalysisStep>('upload');
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [fileId, setFileId] = useState<string>('');
  const [targetRole, setTargetRole] = useState<string>('');
  const [jobDescription, setJobDescription] = useState<string>('');
  const [analysisResult, setAnalysisResult] = useState<ResumeAnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleFileSelect = async (file: File) => {
    setUploadedFile(file);
    setIsLoading(true);

    try {
      console.log('Uploading file:', file.name, 'Size:', file.size);
      const response = await uploadResume(file);
      console.log('Upload response:', response);
      setFileId(response.file_id);
      toast.success('File uploaded successfully!');
      setStep('configure');
    } catch (error: any) {
      console.error('Upload error details:', {
        message: error.message,
        response: error.response,
        status: error.response?.status,
        data: error.response?.data,
      });
      const errorMsg = error.response?.data?.detail || error.message || 'Upload failed';
      toast.error(errorMsg);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAnalyze = async () => {
    if (!fileId) {
      toast.error('Please upload a resume first');
      return;
    }

    setIsLoading(true);
    setStep('analyzing');

    try {
      const result = await analyzeResume({
        file_id: fileId,
        target_role: targetRole || undefined,
        job_description: jobDescription || undefined,
      });

      setAnalysisResult(result);
      setStep('results');
      toast.success('Analysis complete!');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Analysis failed');
      console.error('Analysis error:', error);
      setStep('configure');
    } finally {
      setIsLoading(false);
    }
  };

  const handleStartOver = () => {
    setStep('upload');
    setUploadedFile(null);
    setFileId('');
    setTargetRole('');
    setJobDescription('');
    setAnalysisResult(null);
  };

  const handleExportJSON = () => {
    if (!analysisResult) return;

    const dataStr = JSON.stringify(analysisResult, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `resume-analysis-${analysisResult.analysis_id}.json`;
    link.click();
    URL.revokeObjectURL(url);
    toast.success('JSON exported successfully');
  };

  const handleExportPDF = () => {
    toast('PDF export coming soon!', { icon: '📄' });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-purple-50">
      <Toaster position="top-right" />

      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-br from-primary-500 to-purple-600 p-2 rounded-lg">
                <DocumentTextIcon className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Resume ATS Analyzer
                </h1>
                <p className="text-sm text-gray-600">
                  Blackbox Edition - See how ATS systems read your resume
                </p>
              </div>
            </div>

            {step === 'results' && (
              <button
                onClick={handleStartOver}
                className="btn btn-secondary flex items-center gap-2"
              >
                <ArrowPathIcon className="w-5 h-5" />
                Analyze Another
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Upload Step */}
        {step === 'upload' && (
          <div className="max-w-3xl mx-auto">
            <div className="card">
              <div className="text-center mb-8">
                <SparklesIcon className="w-16 h-16 text-primary-600 mx-auto mb-4" />
                <h2 className="text-3xl font-bold text-gray-900 mb-2">
                  Upload Your Resume
                </h2>
                <p className="text-gray-600">
                  Get instant AI-powered analysis of your resume's ATS compatibility
                </p>
              </div>

              <FileUpload onFileSelect={handleFileSelect} isLoading={isLoading} />

              <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="text-center p-4 bg-primary-50 rounded-lg">
                  <p className="font-semibold text-primary-900 mb-1">
                    ATS Simulation
                  </p>
                  <p className="text-sm text-primary-700">
                    See how systems parse your resume
                  </p>
                </div>
                <div className="text-center p-4 bg-purple-50 rounded-lg">
                  <p className="font-semibold text-purple-900 mb-1">
                    Keyword Analysis
                  </p>
                  <p className="text-sm text-purple-700">
                    Optimize for job descriptions
                  </p>
                </div>
                <div className="text-center p-4 bg-pink-50 rounded-lg">
                  <p className="font-semibold text-pink-900 mb-1">
                    Instant Feedback
                  </p>
                  <p className="text-sm text-pink-700">
                    Get actionable improvements
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Configure Step */}
        {step === 'configure' && (
          <div className="max-w-3xl mx-auto">
            <div className="card">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">
                Optional: Enhance Your Analysis
              </h2>

              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Target Role (Optional)
                  </label>
                  <input
                    type="text"
                    value={targetRole}
                    onChange={(e) => setTargetRole(e.target.value)}
                    placeholder="e.g., Software Engineer, Data Scientist, Product Manager"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    We'll match your resume against this role
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Job Description (Optional)
                  </label>
                  <textarea
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                    placeholder="Paste the job description here for detailed comparison..."
                    rows={8}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Compare your resume directly against the job posting
                  </p>
                </div>

                <div className="flex gap-4">
                  <button
                    onClick={handleStartOver}
                    className="btn btn-secondary flex-1"
                  >
                    Back
                  </button>
                  <button
                    onClick={handleAnalyze}
                    disabled={isLoading}
                    className="btn btn-primary flex-1 flex items-center justify-center gap-2"
                  >
                    {isLoading ? (
                      <>
                        <ArrowPathIcon className="w-5 h-5 animate-spin" />
                        Uploading...
                      </>
                    ) : (
                      <>
                        <SparklesIcon className="w-5 h-5" />
                        Analyze Resume
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Analyzing Step */}
        {step === 'analyzing' && (
          <div className="max-w-3xl mx-auto">
            <div className="card text-center">
              <div className="animate-pulse-slow mb-6">
                <SparklesIcon className="w-20 h-20 text-primary-600 mx-auto" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Analyzing Your Resume...
              </h2>
              <p className="text-gray-600 mb-8">
                Our AI is performing comprehensive analysis. This may take a few moments.
              </p>
              <div className="space-y-3">
                <div className="flex items-center gap-3 justify-center text-gray-700">
                  <div className="w-2 h-2 bg-primary-600 rounded-full animate-bounce" />
                  <span>Parsing document structure</span>
                </div>
                <div className="flex items-center gap-3 justify-center text-gray-700">
                  <div className="w-2 h-2 bg-primary-600 rounded-full animate-bounce delay-100" />
                  <span>Analyzing keywords and content</span>
                </div>
                <div className="flex items-center gap-3 justify-center text-gray-700">
                  <div className="w-2 h-2 bg-primary-600 rounded-full animate-bounce delay-200" />
                  <span>Checking grammar and readability</span>
                </div>
                <div className="flex items-center gap-3 justify-center text-gray-700">
                  <div className="w-2 h-2 bg-primary-600 rounded-full animate-bounce delay-300" />
                  <span>Generating recommendations</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Results Step */}
        {step === 'results' && analysisResult && (
          <ResultsDashboard
            result={analysisResult}
            onExportPDF={handleExportPDF}
            onExportJSON={handleExportJSON}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-gray-600 text-sm">
            Built with ❤️ to help job seekers succeed •{' '}
            <a
              href="https://github.com/thebharathkumar/Resume-Analyser"
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary-600 hover:text-primary-700"
            >
              GitHub
            </a>
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
