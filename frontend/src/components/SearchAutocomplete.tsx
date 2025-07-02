// frontend/src/components/SearchAutocomplete.tsx

import React, { useState, useEffect, useRef } from 'react';
import { gql, useLazyQuery, useMutation } from '@apollo/client';

const GET_SUGGESTIONS = gql`
  query GetSuggestions($term: String!) {
    getSuggestions(term: $term) {
      text
    }
  }
`;

const INCREMENT_SCORE = gql`
  mutation IncrementScore($term: String!) {
    incrementScore(term: $term)
  }
`;

const HighlightedText = ({ text, highlight }: { text: string; highlight: string }) => {
  if (!highlight.trim()) return <span>{text}</span>;
  const regex = new RegExp(`(${highlight})`, 'gi');
  const parts = text.split(regex);
  return (
    <span>
      {parts.map((part, i) =>
        part.toLowerCase() === highlight.toLowerCase() ? <strong key={i}>{part}</strong> : part
      )}
    </span>
  );
};

export default function SearchAutocomplete() {
  const [searchTerm, setSearchTerm] = useState('');
  const [isListVisible, setListVisible] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);
  const wrapperRef = useRef<HTMLDivElement>(null);

  const [getSuggestions, { loading, data }] = useLazyQuery(GET_SUGGESTIONS);
  const [incrementScore] = useMutation(INCREMENT_SCORE);
  
  const suggestions = data?.getSuggestions || [];

  useEffect(() => {
    if (searchTerm.length < 4) {
      setListVisible(false);
      return;
    }
    const debounceTimer = setTimeout(() => {
      getSuggestions({ variables: { term: searchTerm } });
      setListVisible(true);
    }, 150);
    return () => clearTimeout(debounceTimer);
  }, [searchTerm, getSuggestions]);

  useEffect(() => {
    setActiveIndex(-1);
  }, [suggestions]);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target as Node)) {
        setListVisible(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleSuggestionClick = (text: string) => {
    setSearchTerm(text);
    setListVisible(false);
    incrementScore({ variables: { term: text } });
  };

  const handleGoogleSearch = () => {
    const query = searchTerm.trim();
    if (!query) return;
    const encodedQuery = encodeURIComponent(query);
    const googleSearchUrl = `https://www.google.com/search?q=${encodedQuery}`;
    window.open(googleSearchUrl, '_blank', 'noopener,noreferrer');
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    // Se a lista não está visível, deixa o Enter funcionar normalmente (ou para outras funções)
    if (!isListVisible) {
        // Se Enter for pressionado com a lista fechada, busca no Google
        if (e.key === 'Enter') {
            e.preventDefault();
            handleGoogleSearch();
        }
        return;
    }

    // Lógica para quando a lista está visível
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setActiveIndex(prevIndex => (prevIndex + 1) % suggestions.length);
        break;
      case 'ArrowUp':
        e.preventDefault();
        setActiveIndex(prevIndex => (prevIndex - 1 + suggestions.length) % suggestions.length);
        break;
      case 'Enter':
        e.preventDefault(); // Previne qualquer comportamento padrão do Enter
        if (activeIndex >= 0) {
          // Se um item está selecionado, usa a sugestão
          handleSuggestionClick(suggestions[activeIndex].text);
        } else {
          // Se nenhum item estiver selecionado, faz a busca no Google
          handleGoogleSearch();
        }
        break;
      case 'Escape':
        setListVisible(false);
        break;
      default:
        break;
    }
  };

  return (
    <div className="w-full">
      <h2 className="text-2xl font-semibold text-gray-800 dark:text-white mb-1">
        Busca com Autocompletar
      </h2>
      <p className="text-gray-600 dark:text-gray-400 mb-4">
        Digite 4 ou mais caracteres
      </p>

      <div className="relative" ref={wrapperRef}>
        <div className="flex rounded-md shadow-sm">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onFocus={() => { if (searchTerm.length >= 4) setListVisible(true); }}
            onKeyDown={handleKeyDown}
            placeholder="Digite sua busca..."
            autoComplete="off"
            className="flex-grow min-w-0 block w-full px-4 py-3 rounded-l-md border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
          <button 
            type="button" 
            onClick={handleGoogleSearch}
            className="relative inline-flex items-center px-4 py-3 rounded-r-md border border-l-0 border-gray-300 bg-blue-500 text-white font-semibold dark:border-gray-600 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500 sm:text-sm"
          >
            GOOGLE 
          </button>
        </div>

        {isListVisible && (
          <div className="absolute top-full left-0 right-0 z-10 w-full mt-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 rounded-lg shadow-lg min-h-[50px]">
            {loading ? (
              <div className="px-4 py-2.5 text-gray-500 dark:text-gray-400">Buscando...</div>
            ) : (
              suggestions.length > 0 ? (
                <ul className="max-h-80 overflow-y-auto">
                  {suggestions.map((suggestion: { text: string }, index: number) => (
                    <li
                      key={index}
                      onClick={() => handleSuggestionClick(suggestion.text)}
                      onMouseEnter={() => setActiveIndex(index)}
                      ref={el => {
                        if (index === activeIndex && el) {
                          el.scrollIntoView({ block: 'nearest' });
                        }
                      }}
                      className={`px-4 py-2.5 cursor-pointer text-gray-800 dark:text-gray-200 ${
                        index === activeIndex
                          ? 'bg-blue-100 dark:bg-blue-800'
                          : 'hover:bg-gray-100 dark:hover:bg-gray-700'
                      }`}
                    >
                      <HighlightedText text={suggestion.text} highlight={searchTerm} />
                    </li>
                  ))}
                </ul>
              ) : (
                <div className="px-4 py-2.5 text-gray-500 dark:text-gray-400">
                  Nenhuma sugestão encontrada para "<strong>{searchTerm}</strong>"
                </div>
              )
            )}
          </div>
        )}
      </div>
    </div>
  );
}
