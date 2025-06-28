import React from 'react';

const SearchBar = ({ value, onChange }) => {
  return (
    <div className="w-full">
      <input
        type="text"
        className="w-full p-3 text-lg border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:outline-none transition duration-150 ease-in-out"
        placeholder="Digite para buscar..."
        value={value}
        onChange={onChange}
      />
    </div>
  );
};

export default SearchBar;
