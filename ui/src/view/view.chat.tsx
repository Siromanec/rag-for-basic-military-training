import React, {useState} from "react";
import {Box, TextField, Button, Typography, Paper} from "@mui/material";
import { v4 as uuidv4 } from 'uuid';
// Define the types for a message

interface Message {
    sender: "user" | "bot";
    text?: string;
    imageUrl?: string;
    conversationId: string;
}
sessionStorage.setItem("conversationId", uuidv4());
const Chat: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([
        {sender: "bot", text: "Hello! How can I assist you today?", conversationId: sessionStorage.getItem("conversationId") as string},
    ]);
    const [input, setInput] = useState<string>("");

    // Handle sending a message
    const handleSend = () => {
        if (input.trim() === "") return;

        const userMessage: Message = {sender: "user", text: input, conversationId: sessionStorage.getItem("conversationId") as string};
        setMessages((prev) => [...prev, userMessage]);
        setInput("");

        // Simulate bot response
        setTimeout(() => {
            const botMessage: Message = {
                sender: "bot",
                text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In mattis, mi in pellentesque euismod, nulla ante aliquet dui, id feugiat ante augue quis justo. Pellentesque fermentum ligula vel sem scelerisque vehicula ut vitae lorem. Fusce euismod magna et nunc facilisis malesuada. Proin faucibus, ligula non placerat auctor, velit orci consequat enim, a vehicula odio lorem nec turpis. Nunc egestas lacus ligula, nec rutrum enim laoreet non. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Maecenas sagittis tristique nisi ut gravida.\n" +
                    "\n\n" +
                    "Etiam ornare eget justo vel maximus. Suspendisse nibh elit, rhoncus vitae massa suscipit, molestie auctor orci. Suspendisse malesuada sed augue sed sodales. Nam volutpat nunc et tincidunt condimentum. Quisque a eros quis lacus imperdiet condimentum. Nunc congue suscipit consectetur. Curabitur malesuada ante metus, sit amet sollicitudin augue rutrum sit amet. Ut sed tincidunt ligula. Duis eget turpis lacinia, tristique leo in, semper libero. Sed lacinia purus non nibh sagittis pulvinar. Praesent at erat vel erat aliquet blandit. Suspendisse porttitor mollis metus, euismod maximus arcu blandit id.\n" +
                    "\n\n" +
                    "Sed in dui feugiat tellus aliquam sodales vitae non leo. Etiam felis dui, pharetra eu dui ac, vestibulum accumsan mauris. Sed lacus magna, malesuada ut ultrices eget, sodales eget eros. Morbi non lectus eros. Ut dictum eget velit vel tincidunt. Morbi blandit, libero sed vehicula aliquam, velit sapien feugiat justo, vitae eleifend ex neque eget augue. Integer molestie dui neque, ac feugiat lorem maximus vitae. Nunc molestie tincidunt ornare. Nunc vel molestie ligula. Fusce nisl enim, eleifend sit amet diam id, accumsan venenatis tortor. Sed placerat justo eu orci lacinia faucibus vitae vitae sem. Aenean tincidunt, nunc eget finibus aliquam, massa urna porttitor elit, vitae pretium mauris mauris ut lectus. Integer eu est fermentum, eleifend erat sed, viverra purus. Praesent non ex ac ligula lobortis blandit non id sem. Mauris pretium leo diam, non egestas nisi laoreet quis. Aenean rutrum rutrum diam non feugiat.\n" +
                    "\n\n" +
                    "Vestibulum blandit purus vitae aliquet ornare. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam tortor nisi, volutpat id libero in, ultrices egestas arcu. Donec vulputate ac lacus nec ornare. Nullam eget felis est. Aenean porta consequat dolor. Etiam bibendum convallis tristique. Aliquam vulputate blandit nisi, sit amet viverra est pretium sed.\n" +
                    "\n\n" +
                    "Aenean scelerisque posuere turpis in interdum. Fusce posuere nunc sit amet gravida sagittis. Praesent dictum metus tortor, et porta sem tincidunt nec. Morbi condimentum libero urna, eget gravida libero congue sed. Ut a pretium est. Etiam consequat odio nisi, sit amet euismod purus blandit id. Vivamus bibendum consequat vulputate. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Vivamus sed leo eu urna dapibus accumsan. Mauris sed ipsum tellus. Pellentesque quis condimentum nulla.",
                conversationId: sessionStorage.getItem("conversationId") as string
            };
            setMessages((prev) => [...prev, botMessage]);
            setTimeout(() => {
                const botResponses: Message[] = [
                    {sender: "bot", text: "Here's an image for you!", conversationId: sessionStorage.getItem("conversationId") as string},
                    {sender: "bot", imageUrl: "https://via.placeholder.com/500", conversationId: sessionStorage.getItem("conversationId") as string},
                    {sender: "bot", text: "Let me know if you need anything else!", conversationId: sessionStorage.getItem("conversationId") as string},
                ];

                botResponses.forEach((response, index) => {
                    setTimeout(() => {
                        setMessages((prev) => [...prev, response]);
                    }, index * 1000); // Delay each message
                });
            }, 1000);
        }, 1000);
    };

    return (
        <Paper
            elevation={3}
            sx={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
                width: "70%",
                height: "90vh",
                margin: "auto",
                borderRadius: 2,
                overflow: "hidden",
            }}
        >
            {/* Messages Section */}
            <Box
                sx={{
                    flex: 1,
                    overflowY: "auto",
                    padding: 2,
                    backgroundColor: "#bfa991",
                }}
            >
                {messages.map((message, index) => (
                    <Box
                        key={index}
                        sx={{
                            display: "flex",
                            justifyContent:
                                message.sender === "user" ? "flex-end" : "flex-start",
                            marginBottom: 1,
                        }}
                    >
                        <Box
                            sx={{
                                maxWidth: "75%",
                                padding: 1.5,
                                borderRadius: 2,
                                backgroundColor:
                                    message.sender === "user" ? "#8a7e68" : "#584f3e",
                                textAlign: message.sender === "bot" && message.imageUrl ? "center" : "left",
                            }}
                        >
                            {message.text && (
                                <Typography whiteSpace={"pre-wrap"} variant="body1" color={message.sender === "user" ? "black" : "wheat"}>{message.text}</Typography>
                            )}
                            {message.imageUrl && (
                                <Box
                                    component="img"
                                    src={message.imageUrl}
                                    alt="Bot response"
                                    sx={{ maxWidth: "100%", borderRadius: 2, marginTop: 1 }}
                                />
                            )}
                        </Box>
                    </Box>
                ))}
            </Box>

            {/* Input Section */}
            <Box
                sx={{
                    display: "flex",
                    padding: 2,
                    borderTop: "1px solid #584f3e",
                    backgroundColor: "#8a7e68",
                }}
            >
                <TextField
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type your message..."
                    variant="outlined"
                    fullWidth
                    size="small"
                    sx={{marginRight: 1}}
                />
                <Button
                    variant="contained"
                    color="primary"
                    onClick={handleSend}
                    disabled={!input.trim()}
                >
                    Send
                </Button>
            </Box>
        </Paper>
    );
};

export default Chat;
