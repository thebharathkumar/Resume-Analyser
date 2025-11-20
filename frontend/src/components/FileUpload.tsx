import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { ArrowUpTrayIcon, DocumentIcon } from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  isLoading?: boolean;
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileSelect, isLoading }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      if (acceptedFiles.length > 0) {
        const file = acceptedFiles[0];

        // Validate file size (10MB)
        const maxSize = 10 * 1024 * 1024;
        if (file.size > maxSize) {
          toast.error('File too large! Maximum size is 10MB');
          return;
        }

        setSelectedFile(file);
        onFileSelect(file);
        toast.success(`File "${file.name}" selected`);
      }
    },
    [onFileSelect]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/msword': ['.doc'],
    },
    maxFiles: 1,
    disabled: isLoading,
  });

  return (
    <div className="w-full">
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-xl p-12 text-center cursor-pointer
          transition-all duration-200
          ${
            isDragActive
              ? 'border-primary-500 bg-primary-50'
              : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
          }
          ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}
        `}
      >
        <input {...getInputProps()} />

        <div className="flex flex-col items-center space-y-4">
          {selectedFile ? (
            <>
              <DocumentIcon className="w-16 h-16 text-primary-600" />
              <div>
                <p className="text-lg font-semibold text-gray-700">
                  {selectedFile.name}
                </p>
                <p className="text-sm text-gray-500">
                  {(selectedFile.size / 1024).toFixed(2)} KB
                </p>
              </div>
              <p className="text-sm text-gray-500">
                Click or drag to change file
              </p>
            </>
          ) : (
            <>
              <ArrowUpTrayIcon className="w-16 h-16 text-gray-400" />
              <div>
                <p className="text-lg font-semibold text-gray-700">
                  {isDragActive ? 'Drop your resume here' : 'Upload Resume'}
                </p>
                <p className="text-sm text-gray-500 mt-2">
                  Drag and drop or click to select
                </p>
              </div>
              <div className="flex gap-2 text-xs text-gray-400">
                <span className="px-2 py-1 bg-gray-100 rounded">PDF</span>
                <span className="px-2 py-1 bg-gray-100 rounded">DOCX</span>
                <span className="px-2 py-1 bg-gray-100 rounded">DOC</span>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default FileUpload;
