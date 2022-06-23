import { Button, Card, InputAdornment, TextField, Typography } from "@mui/material";
import { AccountCircle, Password } from "@mui/icons-material";

export default function Login(props: {}) {
    return (
        <Card
            sx={{
                position: "absolute",
                top: "50%",
                left: "50%",
                transform: "translate(-50%, -50%)",
                padding: "15px",
            }}
        >
            <Typography
                variant="h5"
                sx={{
                    display: "inline-block",
                    width: "100%",
                    textAlign: "center",
                    marginBottom: "10px",
                }}
            >
                Log In
            </Typography>
            <TextField
                required
                placeholder="Username"
                InputProps={{
                    startAdornment: (
                        <InputAdornment position="start">
                            <AccountCircle />
                        </InputAdornment>
                    ),
                }}
                fullWidth
                sx={{
                    marginBottom: "15px",
                }}
            />
            <TextField
                required
                type="password"
                placeholder="Password"
                InputProps={{
                    startAdornment: (
                        <InputAdornment position="start">
                            <Password />
                        </InputAdornment>
                    ),
                }}
                fullWidth
                sx={{
                    marginBottom: "15px",
                }}
            />
            <Button variant="contained" color="primary" fullWidth>
                Login
            </Button>
        </Card>
    );
}
