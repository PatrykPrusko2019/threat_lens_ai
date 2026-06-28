import { useQuery } from "@tanstack/react-query";

import { getCurrentUser } from "../api/usersApi";


export function useCurrentUser() {
    return useQuery({
        queryKey: ["current-user"],
        queryFn: getCurrentUser,
    });
}