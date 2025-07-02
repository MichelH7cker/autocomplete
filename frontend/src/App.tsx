import SearchAutocomplete from "./components/SearchAutocomplete";
import Header from "./components/Header";

function App() {
  return (
    <div className="w-full min-h-screen bg-gray-100 dark:bg-gray-900">
      <Header />
      <main className="w-full min-h-screen flex items-center justify-center p-4">
        <div className="w-full max-w-2xl">
          <SearchAutocomplete />
        </div>
      </main>

    </div>
  )
}

export default App;
