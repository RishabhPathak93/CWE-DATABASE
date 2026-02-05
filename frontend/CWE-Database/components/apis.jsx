import axios from "axios";

const API_BASE = "http://127.0.0.1:8000/api";

export const findCweTables = async (cweId) => {
  const res = await axios.get(`${API_BASE}/cwe/find/`, {
    params: { cwe_id: cweId },
  });
  return res.data;
};

export const getCweDetails = async (table, cweId) => {
  const res = await axios.get(`${API_BASE}/cwe/details/`, {
    params: {
      table,
      cwe_id: cweId,
    },
  });
  return res.data;
};
