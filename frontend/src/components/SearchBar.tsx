import React from 'react';

export default function SearchVisual() {
  return (
    <div className="w-full">
      <h2 className="text-2xl font-semibold text-gray-800 dark:text-white mb-1">
        Busca com Autocompletar
      </h2>

      <p className="text-gray-600 dark:text-gray-400 mb-4">
        Digite no campo abaixo para exibir as sugestões
      </p>

      <div className="flex rounded-md shadow-sm">
        <input
          type="text"
          placeholder="Digite aqui sua busca..."
          className="flex-grow min-w-0 block w-full px-4 py-3 rounded-l-md border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />
        <button
          type="button"
          className="relative inline-flex items-center px-4 py-3 rounded-r-md border border-l-0 border-gray-300 bg-blue-500 text-white dark:border-gray-600 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500 sm:text-sm"
        >
          BUSCAR
        </button>
      </div>

      <div className="absolute z-10 w-full mt-1 bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-md shadow-lg">
      </div>
    </div>
  );
}
