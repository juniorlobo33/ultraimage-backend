import { useState, useRef } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Upload, Download, Image as ImageIcon, Zap, AlertCircle } from 'lucide-react'
import '../App.css'

// Componente Progress simples
function Progress({ value, className }) {
  return (
    <div className={`w-full bg-gray-200 rounded-full h-2 ${className}`}>
      <div 
        className="bg-blue-600 h-2 rounded-full transition-all duration-300" 
        style={{ width: `${value}%` }}
      ></div>
    </div>
  )
}

function UploadTool() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [progress, setProgress] = useState(0)
  const [processedImageUrl, setProcessedImageUrl] = useState(null)
  const fileInputRef = useRef(null)

  const handleFileSelect = (event) => {
    const file = event.target.files[0]
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file)
      const url = URL.createObjectURL(file)
      setPreviewUrl(url)
      setProcessedImageUrl(null)
    }
  }

  const handleDrop = (event) => {
    event.preventDefault()
    const file = event.dataTransfer.files[0]
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file)
      const url = URL.createObjectURL(file)
      setPreviewUrl(url)
      setProcessedImageUrl(null)
    }
  }

  const handleDragOver = (event) => {
    event.preventDefault()
  }

  const processImage = async () => {
    if (!selectedFile) return

    setIsProcessing(true)
    setProgress(0)

    // Simular processamento
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval)
          setIsProcessing(false)
          // Simular URL da imagem processada
          setProcessedImageUrl(previewUrl) // Em produção, seria a URL retornada pela API
          return 100
        }
        return prev + 10
      })
    }, 300)
  }

  const downloadImage = () => {
    if (processedImageUrl) {
      const link = document.createElement('a')
      link.href = processedImageUrl
      link.download = `upscaled_${selectedFile.name}`
      link.click()
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Ferramenta de Aumento de Resolução
          </h1>
          <p className="text-lg text-gray-600">
            Faça upload de sua imagem e aumente a resolução com IA
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Upload Area */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Upload className="mr-2 h-5 w-5" />
                Upload da Imagem
              </CardTitle>
              <CardDescription>
                Arraste e solte ou clique para selecionar uma imagem
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div
                className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 transition-colors cursor-pointer"
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onClick={() => fileInputRef.current?.click()}
              >
                {previewUrl ? (
                  <div className="space-y-4">
                    <img
                      src={previewUrl}
                      alt="Preview"
                      className="max-w-full max-h-64 mx-auto rounded-lg shadow-md"
                    />
                    <p className="text-sm text-gray-600">
                      {selectedFile?.name}
                    </p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <ImageIcon className="mx-auto h-12 w-12 text-gray-400" />
                    <div>
                      <p className="text-lg font-medium text-gray-900">
                        Clique para fazer upload
                      </p>
                      <p className="text-sm text-gray-600">
                        ou arraste e solte aqui
                      </p>
                    </div>
                    <p className="text-xs text-gray-500">
                      PNG, JPG, JPEG até 10MB
                    </p>
                  </div>
                )}
              </div>
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleFileSelect}
                className="hidden"
              />
              
              {selectedFile && !isProcessing && !processedImageUrl && (
                <Button 
                  onClick={processImage}
                  className="w-full mt-4"
                  size="lg"
                >
                  <Zap className="mr-2 h-5 w-5" />
                  Processar Imagem
                </Button>
              )}
            </CardContent>
          </Card>

          {/* Result Area */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Download className="mr-2 h-5 w-5" />
                Resultado
              </CardTitle>
              <CardDescription>
                Sua imagem processada aparecerá aqui
              </CardDescription>
            </CardHeader>
            <CardContent>
              {isProcessing ? (
                <div className="space-y-4">
                  <div className="text-center">
                    <Zap className="mx-auto h-12 w-12 text-blue-600 animate-pulse" />
                    <p className="mt-2 text-lg font-medium text-gray-900">
                      Processando...
                    </p>
                    <p className="text-sm text-gray-600">
                      Aumentando a resolução com IA
                    </p>
                  </div>
                  <Progress value={progress} className="w-full" />
                  <p className="text-center text-sm text-gray-600">
                    {progress}% concluído
                  </p>
                </div>
              ) : processedImageUrl ? (
                <div className="space-y-4">
                  <img
                    src={processedImageUrl}
                    alt="Processed"
                    className="max-w-full max-h-64 mx-auto rounded-lg shadow-md"
                  />
                  <div className="text-center">
                    <p className="text-sm text-green-600 font-medium mb-2">
                      ✓ Processamento concluído!
                    </p>
                    <Button onClick={downloadImage} className="w-full">
                      <Download className="mr-2 h-4 w-4" />
                      Baixar Imagem
                    </Button>
                  </div>
                </div>
              ) : (
                <div className="text-center py-12">
                  <AlertCircle className="mx-auto h-12 w-12 text-gray-400" />
                  <p className="mt-2 text-lg font-medium text-gray-900">
                    Aguardando upload
                  </p>
                  <p className="text-sm text-gray-600">
                    Faça upload de uma imagem para começar
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Info Cards */}
        <div className="grid md:grid-cols-3 gap-6 mt-8">
          <Card>
            <CardContent className="pt-6">
              <div className="text-center">
                <div className="bg-blue-100 rounded-full p-3 w-fit mx-auto mb-3">
                  <Zap className="h-6 w-6 text-blue-600" />
                </div>
                <h3 className="font-semibold text-gray-900">Rápido</h3>
                <p className="text-sm text-gray-600 mt-1">
                  Processamento em segundos
                </p>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="pt-6">
              <div className="text-center">
                <div className="bg-green-100 rounded-full p-3 w-fit mx-auto mb-3">
                  <ImageIcon className="h-6 w-6 text-green-600" />
                </div>
                <h3 className="font-semibold text-gray-900">Alta Qualidade</h3>
                <p className="text-sm text-gray-600 mt-1">
                  Resultados profissionais
                </p>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="pt-6">
              <div className="text-center">
                <div className="bg-purple-100 rounded-full p-3 w-fit mx-auto mb-3">
                  <AlertCircle className="h-6 w-6 text-purple-600" />
                </div>
                <h3 className="font-semibold text-gray-900">Seguro</h3>
                <p className="text-sm text-gray-600 mt-1">
                  Suas imagens são protegidas
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default UploadTool

