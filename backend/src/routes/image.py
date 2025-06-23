import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext'; // Certifique-se de que este caminho está correto

const UploadTool = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [previewUrl, setPreviewUrl] = useState(null);
    const [uploadProgress, setUploadProgress] = useState(0);
    const [isUploading, setIsUploading] = useState(false);
    const [uploadMessage, setUploadMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [processedImageUrl, setProcessedImageUrl] = useState(null);

    // Configurações do Replicate
    const [scale, setScale] = useState(2); // 2x, 4x
    const [faceEnhance, setFaceEnhance] = useState(false);
    const [denoise, setDenoise] = useState(0.5); // 0.0 to 1.0

    const fileInputRef = useRef(null);
    const dropAreaRef = useRef(null);
    const navigate = useNavigate();
    const { isAuthenticated } = useAuth(); // Usar o contexto de autenticação

    const BACKEND_URL = "https://ultraimage-backend-production.up.railway.app"; // URL do seu backend

    useEffect(( ) => {
        if (!isAuthenticated) {
            navigate('/auth'); // Redireciona para a página de autenticação se não estiver logado
        }
    }, [isAuthenticated, navigate]);

    useEffect(() => {
        const dropArea = dropAreaRef.current;
        if (!dropArea) return;

        const handleDragOver = (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropArea.classList.add('border-blue-500');
        };

        const handleDragLeave = (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropArea.classList.remove('border-blue-500');
        };

        const handleDrop = (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropArea.classList.remove('border-blue-500');
            const files = e.dataTransfer.files;
            if (files && files.length > 0) {
                handleFileChange({ target: { files: files } });
            }
        };

        dropArea.addEventListener('dragover', handleDragOver);
        dropArea.addEventListener('dragleave', handleDragLeave);
        dropArea.addEventListener('drop', handleDrop);

        return () => {
            dropArea.removeEventListener('dragover', handleDragOver);
            dropArea.removeEventListener('dragleave', handleDragLeave);
            dropArea.removeEventListener('drop', handleDrop);
        };
    }, []);

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            setErrorMessage('');
            setUploadMessage('');
            setProcessedImageUrl(null);
            if (file.size > 10 * 1024 * 1024) { // 10MB limit
                setErrorMessage('O arquivo é muito grande. Máximo 10MB.');
                setSelectedFile(null);
                setPreviewUrl(null);
                return;
            }
            const fileType = file.type;
            if (!['image/jpeg', 'image/png', 'image/webp'].includes(fileType)) {
                setErrorMessage('Formato de arquivo não suportado. Use JPG, PNG ou WebP.');
                setSelectedFile(null);
                setPreviewUrl(null);
                return;
            }
            setSelectedFile(file);
            setPreviewUrl(URL.createObjectURL(file));
        } else {
            setSelectedFile(null);
            setPreviewUrl(null);
        }
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            setErrorMessage('Por favor, selecione uma imagem primeiro.');
            return;
        }

        setIsUploading(true);
        setUploadProgress(0);
        setUploadMessage('Enviando imagem...');
        setErrorMessage('');
        setProcessedImageUrl(null);

        const formData = new FormData();
        formData.append('image', selectedFile);
        formData.append('scale', scale);
        formData.append('face_enhance', faceEnhance);
        formData.append('denoise', denoise);

        try {
            const response = await fetch(`${BACKEND_URL}/api/image/upload`, {
                method: 'POST',
                body: formData,
                // No need to set Content-Type for FormData, browser does it automatically
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Erro no processamento. Tente novamente.');
            }

            const data = await response.json();
            setUploadMessage('Processamento concluído!');
            setProcessedImageUrl(data.imageUrl); // A imagem processada vem em base64
            setUploadProgress(100);
        } catch (error) {
            console.error('Erro ao fazer upload:', error);
            setErrorMessage(error.message || 'Erro desconhecido ao processar a imagem.');
            setUploadProgress(0);
        } finally {
            setIsUploading(false);
        }
    };

    const handleDownload = () => {
        if (processedImageUrl) {
            const link = document.createElement('a');
            link.href = processedImageUrl;
            link.download = `ultraimageai_enhanced_${Date.now()}.png`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
            <h1 className="text-4xl font-bold text-gray-800 mb-8">Ferramenta de Melhoria de Imagens</h1>

            <div
                ref={dropAreaRef}
                className="w-full max-w-2xl p-8 border-2 border-dashed border-gray-300 rounded-lg text-center cursor-pointer hover:border-blue-500 transition-colors duration-200 bg-white shadow-md"
                onClick={() => fileInputRef.current.click()}
            >
                <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFileChange}
                    className="hidden"
                    accept="image/jpeg, image/png, image/webp"
                />
                {previewUrl ? (
                    <img src={previewUrl} alt="Preview" className="max-h-64 mx-auto mb-4 rounded-md shadow-sm" />
                ) : (
                    <div className="text-gray-500">
                        <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
                            <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                        <p className="mt-1 text-sm">Arraste sua imagem aqui, ou clique para selecionar</p>
                        <p className="text-xs text-gray-400">JPG, PNG ou WebP (Máx. 10MB)</p>
                    </div>
                )}
            </div>

            {errorMessage && (
                <p className="text-red-500 mt-4">{errorMessage}</p>
            )}

            {selectedFile && (
                <div className="w-full max-w-2xl mt-6 p-6 bg-white rounded-lg shadow-md">
                    <h2 className="text-xl font-semibold mb-4 text-gray-700">Configurações de Processamento</h2>
                    
                    <div className="mb-4">
                        <label htmlFor="scale" className="block text-sm font-medium text-gray-700">Escala de Aumento (Upscale)</label>
                        <select
                            id="scale"
                            className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                            value={scale}
                            onChange={(e) => setScale(parseInt(e.target.value))}
                            disabled={isUploading}
                        >
                            <option value={2}>2x (Recomendado)</option>
                            <option value={4}>4x (Pode ser mais lento e consumir mais memória)</option>
                        </select>
                    </div>

                    <div className="mb-4 flex items-center">
                        <input
                            id="faceEnhance"
                            type="checkbox"
                            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                            checked={faceEnhance}
                            onChange={(e) => setFaceEnhance(e.target.checked)}
                            disabled={isUploading}
                        />
                        <label htmlFor="faceEnhance" className="ml-2 block text-sm font-medium text-gray-700">Melhorar Rostos (Face Enhance)</label>
                    </div>

                    <div className="mb-4">
                        <label htmlFor="denoise" className="block text-sm font-medium text-gray-700">Remoção de Ruído (Denoise)</label>
                        <input
                            id="denoise"
                            type="range"
                            min="0.0"
                            max="1.0"
                            step="0.1"
                            value={denoise}
                            onChange={(e) => setDenoise(parseFloat(e.target.value))}
                            className="mt-1 block w-full"
                            disabled={isUploading}
                        />
                        <span className="text-sm text-gray-500">{denoise.toFixed(1)}</span>
                    </div>

                    <button
                        onClick={handleUpload}
                        className={`w-full py-3 px-6 rounded-md text-white font-semibold transition-colors duration-200 ${
                            isUploading
                                ? 'bg-gray-400 cursor-not-allowed'
                                : 'bg-blue-600 hover:bg-blue-700'
                        }`}
                        disabled={isUploading}
                    >
                        {isUploading ? 'Processando...' : 'Processar com IA'}
                    </button>

                    {isUploading && (
                        <div className="w-full bg-gray-200 rounded-full h-2.5 mt-4">
                            <div
                                className="bg-blue-600 h-2.5 rounded-full"
                                style={{ width: `${uploadProgress}%` }}
                            ></div>
                        </div>
                    )}

                    {uploadMessage && (
                        <p className="text-green-600 mt-4 text-center">{uploadMessage}</p>
                    )}
                </div>
            )}

            {processedImageUrl && (
                <div className="w-full max-w-2xl mt-8 p-6 bg-white rounded-lg shadow-md text-center">
                    <h2 className="text-xl font-semibold mb-4 text-gray-700">Imagem Processada</h2>
                    <img src={processedImageUrl} alt="Processed" className="max-h-96 mx-auto mb-4 rounded-md shadow-sm border border-gray-200" />
                    <button
                        onClick={handleDownload}
                        className="bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded-md font-semibold transition-colors duration-200"
                    >
                        Baixar Imagem Melhorada
                    </button>
                </div>
            )}
        </div>
    );
};

export default UploadTool;
