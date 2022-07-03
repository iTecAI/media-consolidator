import {
    Book,
    Download,
    MusicNote,
    OpenInNew,
    Podcasts,
    Search,
    Tsunami,
    YouTube,
} from "@mui/icons-material";
import {
    Divider,
    TextField,
    InputAdornment,
    ButtonGroup,
    Button,
    Card,
    CardContent,
    CardHeader,
    Paper,
    IconButton,
    Tooltip,
    Avatar,
    Badge,
} from "@mui/material";
import { Box } from "@mui/material";
import { useEffect, useState } from "react";
import { get } from "../../util/api";
import "./index.scss";

type ActiveMode = "torrents" | "podcasts" | "youtube" | "music" | "books";
//const modes: ActiveMode[] = ["torrents", "podcasts", "youtube", "music", "books"];
const ModeIcons: { [key: string]: any } = {
    torrents: <Tsunami fontSize="small" />,
    podcasts: <Podcasts fontSize="small" />,
    youtube: <YouTube fontSize="small" />,
    music: <MusicNote fontSize="small" />,
    books: <Book fontSize="small" />,
};

function ModeButton(props: {
    mode: ActiveMode;
    activeModes: ActiveMode[];
    setActiveModes: (modes: ActiveMode[]) => void;
    onChange?: (activeModes: ActiveMode[]) => void;
}) {
    let { mode, activeModes, setActiveModes } = props;
    return (
        <Button
            variant={activeModes.includes(mode) ? "contained" : "outlined"}
            onClick={() => {
                let newModes: ActiveMode[] = [];
                if (activeModes.includes(mode)) {
                    for (let m of activeModes) {
                        if (m !== mode) {
                            newModes.push(m);
                        }
                    }
                } else {
                    newModes = JSON.parse(JSON.stringify(activeModes));
                    newModes.push(mode);
                }
                setActiveModes(newModes);
                props.onChange ? props.onChange(newModes) : (() => {})();
            }}
        >
            {mode}
        </Button>
    );
}

type SearchResultModel = {
    title: string;
    subtitle: string;
    description: string;
    image: string;
    type: ActiveMode;
    reference: string | number;
    canDownload: boolean;
    canExpand: boolean;
    similarity: number;
};

function SearchResult(props: SearchResultModel) {
    return (
        <Card key={props.type + props.reference.toString()} sx={{ margin: "10px" }}>
            <CardHeader
                avatar={
                    <Badge
                        overlap="circular"
                        anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
                        badgeContent={ModeIcons[props.type]}
                    >
                        <Avatar src={props.image} alt={props.title}>
                            {ModeIcons[props.type]}
                        </Avatar>
                    </Badge>
                }
                title={props.title}
                subheader={props.subtitle}
                className="noselect"
                action={
                    <>
                        {props.canDownload && (
                            <Tooltip title="Download">
                                <IconButton>
                                    <Download />
                                </IconButton>
                            </Tooltip>
                        )}
                        {props.canExpand && (
                            <Tooltip title="Expand">
                                <IconButton>
                                    <OpenInNew />
                                </IconButton>
                            </Tooltip>
                        )}
                    </>
                }
            />
            <CardContent sx={{ position: "relative", boxSizing: "border-box" }}>
                <Paper
                    variant="outlined"
                    sx={{
                        padding: "15px",
                    }}
                >
                    {props.description}
                </Paper>
            </CardContent>
        </Card>
    );
}

export default function IndexPage() {
    const [activeModes, setActiveModes] = useState([] as ActiveMode[]);
    const [results, setResults] = useState([] as any[]);
    const [searchValue, setSearchValue] = useState("");
    const [toSearch, setToSearch] = useState("");

    useEffect(() => {
        if (toSearch === "") {
            return;
        }
        let newResults: any[] = [];
        for (let mode of activeModes) {
            switch (mode) {
                case "podcasts":
                    get<SearchResultModel[]>({
                        path: "/sources/podcasts/search",
                        query: { q: toSearch },
                    }).then((result) => {
                        if (result.success) {
                            newResults.push(...result.value.map((v) => <SearchResult {...v} />));
                        }
                    });
            }
        }
        setResults(newResults.sort((a, b) => b.similarity - a.similarity));
    }, [activeModes, toSearch, searchValue]);

    return (
        <Box sx={{ width: "100%", height: "100%" }}>
            <Box sx={{ height: "48px", position: "relative" }}>
                <TextField
                    InputProps={{
                        startAdornment: (
                            <InputAdornment position="start">
                                <Search />
                            </InputAdornment>
                        ),
                    }}
                    variant="outlined"
                    size="small"
                    placeholder="Search"
                    className="main-search"
                    onKeyDown={(event) => {
                        if (event.key === "Enter") {
                            setToSearch(searchValue);
                        }
                    }}
                    value={searchValue}
                    onChange={(event) => setSearchValue(event.target.value)}
                />
                <ButtonGroup className="mode-buttons">
                    <ModeButton
                        mode={"torrents"}
                        activeModes={activeModes}
                        setActiveModes={setActiveModes}
                        onChange={(activeModes) => setToSearch(searchValue)}
                    />
                    <ModeButton
                        mode={"podcasts"}
                        activeModes={activeModes}
                        setActiveModes={setActiveModes}
                        onChange={(activeModes) => setToSearch(searchValue)}
                    />
                    <ModeButton
                        mode={"youtube"}
                        activeModes={activeModes}
                        setActiveModes={setActiveModes}
                        onChange={(activeModes) => setToSearch(searchValue)}
                    />
                    <ModeButton
                        mode={"music"}
                        activeModes={activeModes}
                        setActiveModes={setActiveModes}
                        onChange={(activeModes) => setToSearch(searchValue)}
                    />
                    <ModeButton
                        mode={"books"}
                        activeModes={activeModes}
                        setActiveModes={setActiveModes}
                        onChange={(activeModes) => setToSearch(searchValue)}
                    />
                </ButtonGroup>
            </Box>
            <Divider />
            <Box sx={{ height: "calc(100% - 49px)", width: "100%", overflowY: "auto" }}>
                {results}
            </Box>
        </Box>
    );
}
