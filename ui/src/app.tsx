import { DataGrid, type GridColDef } from "@mui/x-data-grid";
import dateformat from "dateformat";
import { parseAsInteger, parseAsString, parseAsStringEnum, useQueryStates } from "nuqs";
import { useMemo } from "react";
import { $api } from "./api";
import type { components } from "./api/generated";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "./components/ui/tooltip";

const columns: GridColDef<components["schemas"]["Product"]>[] = [
  {
    field: "title",
    headerName: "Product Name",
    flex: 1,
    renderCell: ({ value, row }) => (
      <div className="flex items-center gap-2">
        <Tooltip>
          <TooltipTrigger>
            <img src={row.image_url} alt={value} className="size-14 aspect-square" />
          </TooltipTrigger>
          <TooltipContent side="right" className="bg-background border shadow">
            <img src={row.image_url} alt={value} className="size-100 aspect-square" />
          </TooltipContent>
        </Tooltip>
        <a
          href={row.product_url}
          target="_blank"
          rel="noopener noreferrer"
          className="underline text-primary"
        >
          {value}
        </a>
      </div>
    ),
  },
  {
    field: "brand",
    headerName: "Brand",
    flex: 0.1,
  },
  {
    field: "price_max",
    headerName: "Price (PHP)",
    type: "number",
    flex: 0.1,
  },
  {
    field: "domain_tld",
    headerName: "Etailer",
    flex: 0.1,
    valueFormatter: (v: components["schemas"]["Product"]["domain_tld"]) =>
      v.split(".")[0],
    cellClassName: "capitalize",
  },
  {
    field: "variants",
    headerName: "In Stock",
    flex: 0.1,
    type: "boolean",
    valueGetter: (v: components["schemas"]["ProductVariant"][]) =>
      v.some((v) => v.is_available),
  },
];

function App() {
  const [{ page, pageSize, sortBy, sortOrder }, setState] = useQueryStates({
    page: parseAsInteger.withDefault(1),
    pageSize: parseAsInteger.withDefault(10),
    sortBy: parseAsString.withDefault("price_max"),
    sortOrder: parseAsStringEnum(["asc", "desc"]).withDefault("desc"),
  });

  const { data: products, isLoading } = $api.useQuery("get", "/products", {
    params: {
      query: {
        page,
        page_size: pageSize,
        sort_by: sortBy,
        sort_order: sortOrder,
      },
    },
  });

  const lastUpdate = useMemo(() => products?.meta.last_data_update, [products]);
  const rowCount = useMemo(() => products?.meta.total_count, [products]);

  return (
    <main className="min-h-screen w-screen p-6">
      <div className="flex flex-col gap-4">
        <p>
          <b>Last update: </b>
          {lastUpdate && dateformat(lastUpdate, "yyyy-mm-dd HH:MM:ss")} (local time)
        </p>
        <TooltipProvider>
          <DataGrid
            rows={products?.data ?? []}
            columns={columns}
            loading={isLoading}
            pagination
            paginationMode="server"
            pageSizeOptions={[10, 25]}
            paginationModel={{ page: page - 1, pageSize }}
            onPaginationModelChange={({ page, pageSize }) => {
              setState({ page: page + 1, pageSize });
            }}
            sortingMode="server"
            sortModel={[{ field: sortBy, sort: sortOrder }]}
            onSortModelChange={(model) => {
              console.debug(model);
              if (model.length === 0) {
                setState({ sortBy: null, sortOrder: null });
              } else {
                setState({ sortBy: model[0].field, sortOrder: model[0].sort });
              }
            }}
            filterMode="server"
            rowCount={rowCount}
          />
        </TooltipProvider>
      </div>
    </main>
  );
}

export default App;
