import { useEffect, useState } from "react";
import { Avatar, CircularProgress, Grid } from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import dateFormat from "dateformat";
import api from "./api";
import "./App.css";

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const cols = [
    {
      field: "name",
      headerName: "Name",
      flex: 1,
      renderCell: ({ row, value }) => (
        <>
          <Avatar src={row.image_url} alt={value} variant="square" sx={{ padding: 0 }} />
          <a href={row.url} target="_blank" rel="noopener noreferrer" style={{ padding: "0.5em" }}>
            {value}
          </a>
        </>
      ),
    },
    {
      field: "price",
      headerName: `Price (PHP, last updated ${dateFormat(new Date(`${data.updated}Z`), "yyyy mmm d h:MM TT")})`,
      type: "number",
      flex: 0.5,
    },
    {
      field: "platform",
      headerName: "Platform",
    },
    {
      field: "seller",
      headerName: "Seller",
      valueFormatter: ({ value }) => (value == null ? "—" : value),
      minWidth: 200,
    },
    {
      field: "stock",
      headerName: "Remaining Stock",
      type: "number",
      minWidth: 150,
      valueFormatter: ({ value }) => (value == null ? "—" : value),
    },
    {
      field: "sold",
      headerName: "Sold Stock",
      type: "number",
      valueFormatter: ({ value }) => (value == null ? "—" : value),
    },
    {
      field: "rating",
      headerName: "Rating (Reviews)",
      minWidth: 150,
      type: "number",
      renderCell: ({ row, value }) => `${value.toFixed(2)} (${row.reviews})`,
    },
  ];

  useEffect(() => {
    setLoading(true);
    api
      .get()
      .then(res => setData(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  return (
    <Grid container alignItems="center" justifyContent="center" xs={12} height="97vh">
      {loading ? (
        <CircularProgress size={50} disableShrink />
      ) : (
        <DataGrid
          columns={cols}
          rows={data.data}
          disableSelectionOnClick
          density="comfortable"
          components={{
            Toolbar: GridToolbar,
          }}
        />
      )}
    </Grid>
  );
}

export default App;
