import "./App.scss";
import { createTheme, Theme, ThemeProvider } from "@mui/material";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Layout } from "./pages/layout/Layout";
import Login from "./pages/login/Login";
import IndexPage from "./pages/index/Index";

export const theme: Theme = createTheme({
    palette: {
        mode: "dark",
        primary: {
            main: "#8f3dce",
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
                                <Layout showLogout>
                                    <IndexPage />
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
