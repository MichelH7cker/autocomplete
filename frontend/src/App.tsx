import SearchAutocomplete from "./components/SearchAutocomplete";

function App() {
  return (
    <div className="w-full min-h-screen flex items-center justify-center bg-gray-100 dark:bg-gray-900 p-4">
      <div className="w-full max-w-2xl">
        <SearchAutocomplete />
      </div>
    </div>
  )
}

export default App;
