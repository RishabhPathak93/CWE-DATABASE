import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { findCweTables } from "../components/apis";

const ITEMS_PER_PAGE = 8;

const TablesListPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const cweId = new URLSearchParams(location.search).get("cwe");

  const [tables, setTables] = useState([]);
  const [page, setPage] = useState(1);

  useEffect(() => {
    if (!cweId) return;

    findCweTables(cweId).then((data) => {
      setTables(data.tables || []);
    });
  }, [cweId]);

  const start = (page - 1) * ITEMS_PER_PAGE;
  const paginatedTables = tables.slice(start, start + ITEMS_PER_PAGE);
  const totalPages = Math.ceil(tables.length / ITEMS_PER_PAGE);

  return (
    <div className="page list-container">
      {/* Back to Search Button */}
      <button className="back-btn-small" onClick={() => navigate("/")}>
        ← New Search
      </button>

      <h2>Tables containing CWE-{cweId}</h2>

      <div className="cards-wrapper">
    {paginatedTables.map((table) => (
        <div key={table} className="card" onClick={() => navigate(`/finding?cwe=${cweId}&table=${table}`)}>
            {table.replace(/_/g, ' ')}
        </div>
    ))}
</div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="pagination">
          <button 
            className="pagi-btn" 
            disabled={page === 1} 
            onClick={() => setPage(page - 1)}
          >
            Prev
          </button>

          <span className="page-info">
            Page <b>{page}</b> of <b>{totalPages}</b>
          </span>

          <button
            className="pagi-btn"
            disabled={page === totalPages || totalPages === 0}
            onClick={() => setPage(page + 1)}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default TablesListPage;