import "./App.scss";
import { createTheme, Theme, ThemeProvider } from "@mui/material";
import { BrowserRouter, Outlet, Route, Routes } from "react-router-dom";
import { Layout } from "./pages/layout/Layout";
import Login from "./pages/login/Login";

export const theme: Theme = createTheme({
    palette: {
        mode: "dark",
        primary: {
            main: "#5d2985",
        },
        secondary: {
            main: "#f50057",
        },
        background: {
            default: "#2d2d2d",
            paper: "#353535",
        },
    },
});

function App() {
    return (
        <ThemeProvider theme={theme}>
            <div className="root">
                <BrowserRouter>
                    <Routes>
                        <Route
                            path="/"
                            element={
                                <Layout showTabs showLogout>
                                    <Outlet />
                                </Layout>
                            }
                        ></Route>
                        <Route
                            path="/login"
                            element={
                                <Layout>
                                    <Login />
                                </Layout>
                            }
                        />
                    </Routes>
                </BrowserRouter>
            </div>
        </ThemeProvider>
    );
}

export default App;
