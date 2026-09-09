import { useState } from 'react'
import './App.css'

function App() {
  const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [contentType, setContentType] = useState("quiz");

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);      // on réinitialise l'erreur précédente
    setResult(null);       // on efface l'ancien quiz
    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("content_type", contentType);
      const response = await fetch(`${API_URL}/generate-content`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
      throw new Error("La génération a échoué côté serveur");
      }

      const data = await response.json();
      setResult(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }

  };

  return (
    <div className="min-h-screen bg-gray-900 py-10">
      <div className="max-w-2xl mx-auto bg-gray-800 rounded-lg shadow p-6">
      <h1 className="text-3xl font-bold text-gray-100 mb-2">Générateur de contenu Pédagogique</h1>
      <p className="text-gray-400 mb-4">Uploadez un cours pour générer le contenu souhaité automatiquement.</p>
      <div className="flex items-center gap-3 mb-4">
        <select
          value={contentType}
          onChange={(e) => {
            setContentType(e.target.value);
            setResult(null);
          }}
          className="bg-gray-700 text-gray-200 px-4 py-2 rounded"
        >
          <option value="quiz">Quiz</option>
          <option value="flashcard">Fiche de synthèse</option>
        </select>
        <label className="inline-block cursor-pointer bg-gray-700 text-gray-200 px-4 py-2 rounded hover:bg-gray-600">
          {file ? file.name : "Choisir un fichier"}
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            className="hidden"
          />
        </label>
        <button
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:bg-gray-700 disabled:text-gray-500 disabled:cursor-not-allowed disabled:opacity-60"
          disabled={!file || loading}
          onClick={handleSubmit}>
          Générer le contenu
        </button>
      </div>
      

      {loading && contentType === "quiz" && <p className="mt-4 text-gray-600">Génération du quiz en cours...</p>}
      {loading && contentType === "flashcard" && <p className="mt-4 text-gray-600">Génération de la fiche de synthese en cours...</p>}
      {error && <p className="mt-4 text-red-600">Erreur : {error}</p>}

      {result && contentType === "quiz" && (
        <div className="mt-6">
          {result.quiz.map((question, index) => (
            <div className="border border-gray-700 rounded-lg p-4 mb-4 bg-gray-800 shadow-sm" key={index}>
              <h3 className="font-semibold text-gray-100 mb-2">Question {index + 1} : {question.question}</h3>
              <ul className="mb-2 space-y-1">
                {question.options.map((option, i) => (
                  <li key={i} className={i === question.correct_answer ? "font-bold text-green-400" : "text-gray-300"}>
                    {option}
                  </li>
                ))}
              </ul>
              <p className="text-sm text-gray-500 italic">{question.explanation}</p>
            </div>
          ))}
        </div>
        )}
        {result && contentType === "flashcard" && (
        <div className="mt-6">
          {result.sections.map((section, index) => (
            <div className="border border-gray-700 rounded-lg p-4 mb-4 bg-gray-800" key={index}>
              <h3 className="font-semibold text-gray-100 mb-2">{section.title}</h3>
              <p className="text-gray-300">{section.content}</p>
            </div>
          ))}
        </div>
        )}
      </div>
    </div>
  )
}

export default App
