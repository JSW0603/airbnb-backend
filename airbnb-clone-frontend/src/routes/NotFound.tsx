import {Button, Heading, Text, VStack} from "@chakra-ui/react";
import {Link} from "react-router-dom";

export default function NotFound() {
    return (
        <VStack bg="gray.100" minH="100vh" justifyContent={"center"} alignItems={"center"}>
            <Heading>Page not Found.</Heading>
            <Text>You are in the wrong place.</Text>
            <Link to={"/"}>
                <Button colorScheme={"red"} variant={"outline"}>Go Home</Button>
            </Link>
        </VStack>
    );
}