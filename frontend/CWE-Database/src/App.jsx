import { BrowserRouter, Routes, Route } from "react-router-dom";
import SearchPage from "../pages/search_Page";
import TablesListPage from "../pages/Tables_list_Page";
import FindingPage from "../pages/Finding_Page";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<SearchPage />} />
        <Route path="/tables" element={<TablesListPage />} />
        <Route path="/finding" element={<FindingPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
