import { QueryClient } from "@tanstack/react-query";
import axios from "axios";
import createFetchClient from "openapi-fetch";
import createClient from "openapi-react-query";
import type { paths } from "./generated";

const baseURL = "/api/";

export const axi = axios.create({ baseURL });

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnMount: true,
      refetchOnReconnect: true,
      refetchOnWindowFocus: true,
      retry: 3,
      retryDelay: (failureCount) => Math.min(1000 * 2 ** failureCount, 30000),
    },
    mutations: {
      retry: false,
    },
  },
});

export const fetchClient = createFetchClient<paths>({
  baseUrl: "/api",
});

export const $api = createClient(fetchClient);
