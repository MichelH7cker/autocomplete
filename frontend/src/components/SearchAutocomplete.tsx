import { useState, useEffect, useRef } from 'react';
import { gql, useLazyQuery } from '@apollo/client';

const GET_SUGGESTIONS = gql`
  query GetSuggestions($term: String!) {
    getSuggestions(term: $term) {
      text
    }
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
  const wrapperRef = useRef<HTMLDivElement>(null);

  const [getSuggestions, { loading, data }] = useLazyQuery(GET_SUGGESTIONS);
  const suggestions = data?.getSuggestions || [];

  useEffect(() => {
    if (searchTerm.length < 4) {
      setListVisible(false);
      return;
    }
    const debounceTimer = setTimeout(() => {
      getSuggestions({ variables: { term: searchTerm } });
    }, 300);
    return () => clearTimeout(debounceTimer);
  }, [searchTerm, getSuggestions]);

  useEffect(() => {
    if (suggestions.length > 0) setListVisible(true);
    else setListVisible(false);
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
  };

  return (
    <div className="w-full" ref={wrapperRef}>
      <h2 className="text-2xl font-semibold text-gray-800 dark:text-white mb-1">
        Busca com Autocompletar
      </h2>
      <p className="text-gray-600 dark:text-gray-400 mb-4">
        Digite 4 ou mais caracteres
      </p>

      <div className="flex rounded-md shadow-sm">
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          onFocus={() => { if (suggestions.length > 0) setListVisible(true); }}
          placeholder="Digite sua busca..."
          className="flex-grow min-w-0 block w-full px-4 py-3 rounded-l-md border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />
        <button type="button" className="relative inline-flex items-center px-4 py-3 rounded-r-md border border-l-0 border-gray-300 bg-blue-500 text-white font-semibold dark:border-gray-600 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500 sm:text-sm">
          BUSCAR
        </button>
      </div>

      {isListVisible && (
        <div className="w-full mt-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 rounded-lg shadow-lg">
          {loading ? (
            <div className="px-4 py-2.5 text-gray-500 dark:text-gray-400">Buscando...</div>
          ) : (
            <ul className="max-h-80 overflow-y-auto">
              {suggestions.map((suggestion: { text: string }, index: number) => (
                <li
                  key={index}
                  onClick={() => handleSuggestionClick(suggestion.text)}
                  className="px-4 py-2.5 cursor-pointer text-gray-800 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700"
                >
                  <HighlightedText text={suggestion.text} highlight={searchTerm} />
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}
