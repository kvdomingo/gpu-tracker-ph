import { useEffect, useState } from "react";
import { Avatar, CircularProgress, Grid, Paper, Popper } from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { Check, Clear } from "@mui/icons-material";
import dateFormat from "dateformat";
import api from "./api";
import "./App.css";

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [anchorEl, setAnchorEl] = useState(null);
  const [hoverRow, setHoverRow] = useState(null);
  const cols = [
    {
      field: "name",
      headerName: "Name",
      flex: 1,
      renderCell: ({ row, value }) => (
        <>
          <Avatar
            src={row.image_url}
            alt={value}
            variant="square"
            sx={{ padding: 0 }}
            onMouseEnter={e => {
              setAnchorEl(e.currentTarget);
              setHoverRow(row);
            }}
            onMouseLeave={() => {
              setAnchorEl(null);
              setHoverRow(null);
            }}
          />
          <a href={row.url} target="_blank" rel="noopener noreferrer" style={{ padding: "0.5em" }}>
            {value}
          </a>
        </>
      ),
    },
    {
      field: "price",
      headerName: `Price (PHP${
        !!data.updated ? ", last updated " + dateFormat(new Date(data.updated), "yyyy mmm d h:MM TT") : ""
      })`,
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
      field: "official_store",
      headerName: "Official Store",
      type: "boolean",
      renderCell: ({ value }) => (value === null ? "—" : value ? <Check /> : <Clear />),
      minWidth: 125,
    },
    {
      field: "verified_seller",
      headerName: "Verified Seller",
      type: "boolean",
      renderCell: ({ value }) => (value === null ? "—" : value ? <Check /> : <Clear />),
      minWidth: 125,
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
        <>
          <DataGrid
            columns={cols}
            rows={data.data}
            disableSelectionOnClick
            density="comfortable"
            components={{
              Toolbar: GridToolbar,
            }}
          />
          <Popper open={Boolean(anchorEl)} anchorEl={anchorEl} placement="left-start">
            <Paper sx={{ padding: 0 }}>
              <img src={hoverRow?.image_url} alt={hoverRow?.name} height={500} />
            </Paper>
          </Popper>
        </>
      )}
    </Grid>
  );
}

export default App;
