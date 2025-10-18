import React, { createContext, useContext, useEffect, useState } from "react";
import { authAPI } from "../api/auth";
import api from "../api/index";

const AuthContext = createContext();

export function useAuth() {
  return useContext(AuthContext);
}

/**
 * AuthProvider
 * - Restores session on mount using /auth/refresh -> /api/me
 * - Exposes: user, setUser, loading, login(), logout()
 *
 * NOTE: accessToken is stored in localStorage in this example for simplicity.
 * Prefer in-memory storage for better security in production.
 */
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null); // null = not logged in, object = logged in
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        // Check if we have a stored token
        if (authAPI.isAuthenticated()) {
          // Attempt to refresh token
          await authAPI.refreshToken();

          // Try to fetch user data
          const meRes = await api.get('/api/me/');
          
          if (mounted) {
            const data = meRes.data;
            console.log("AuthProvider - /api/me/ response:", data);
            console.log("AuthProvider - extracted full_name:", data.account?.full_name);
            
            const userData = {
              name: data.account?.full_name || "User",
              email: data.account?.email || "",
              avatar: data.account?.avatar || null,
              isLoggedIn: true,
              profileCompleted: !!data.profileCompleted,
              userId: data.account?.user_id || null,
            };
            console.log("AuthProvider - setting user data:", userData);
            setUser(userData);
          }
        } else {
          setUser(null);
        }
      } catch (err) {
        console.warn("Session restore failed:", err);
        setUser(null);
      } finally {
        if (mounted) setLoading(false);
      }
    })();

    return () => {
      mounted = false;
    };
  }, []);

  // login helper — call after successful /auth/login response
  const login = ({ accessToken, fullName, email, avatar = null, profileCompleted = false, userId = null }) => {
    console.log("AuthProvider - login called with:", { accessToken: !!accessToken, fullName, email, avatar, profileCompleted, userId });
    
    if (accessToken) localStorage.setItem("accessToken", accessToken);
    
    const userData = {
      name: fullName || email?.split?.("@")?.[0] || "User",
      email: email || "",
      avatar,
      isLoggedIn: true,
      profileCompleted: !!profileCompleted,
      userId: userId || null,
    };
    console.log("AuthProvider - login setting user:", userData);
    setUser(userData);
  };

  // logout helper — revokes on server and clears local state
  const logout = async () => {
    try {
      await authAPI.logout();
    } catch (err) {
      console.warn("Logout request failed:", err);
    } finally {
      setUser(null);
    }
  };

  const value = { user, setUser, login, logout, loading };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
