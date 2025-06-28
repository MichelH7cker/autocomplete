import React from 'react';

const getHighlightedText = (text, highlight) => {
  const parts = text.split(new RegExp(`(${highlight})`, 'gi'));
  return (
    <span>
      {parts.map((part, i) =>
        part.toLowerCase() === highlight.toLowerCase() ? <strong key={i} className="font-bold">{part}</strong> : part
      )}
    </span>
  );
};

const SuggestionsList = ({ suggestions, searchTerm, onSuggestionClick }) => {
  if (suggestions.length === 0) {
    return null;
  }

  return (
    <ul className="absolute w-full bg-white border border-gray-300 rounded-b-lg mt-1 shadow-lg max-h-60 overflow-y-auto z-10">
      {suggestions.slice(0, 10).map((suggestion, index) => (
        <li
          key={index}
          className="p-3 cursor-pointer hover:bg-slate-100 transition duration-150 ease-in-out"
          onClick={() => onSuggestionClick(suggestion)}
        >
          {getHighlightedText(suggestion, searchTerm)}
        </li>
      ))}
    </ul>
  );
};

export default SuggestionsList;
