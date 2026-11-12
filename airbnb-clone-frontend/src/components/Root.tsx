import { Link, Outlet } from "react-router-dom";
import { SiAirbnb } from "react-icons/si";
import { CiUser, CiDark, CiSun } from "react-icons/ci";
import { Box, Button, HStack, IconButton, useColorMode, useColorModeValue, 
    Modal, ModalOverlay, ModalContent, ModalHeader, ModalCloseButton, 
    ModalBody, Input, InputGroup, InputLeftElement, useDisclosure, VStack } from "@chakra-ui/react";

export default function Root() {
    const { toggleColorMode } = useColorMode();
    const Icon = useColorModeValue (<CiDark />, <CiSun />);
    const { isOpen, onOpen, onClose } = useDisclosure();
    return (
        <Box>
            <HStack justifyContent={"space-between"} px={10} py={5} borderBottomWidth={1}>
                <Box color ={"red.500"} fontSize={"2xl"} fontWeight={"bold"}>
                    <Link to={"/"}>
                        <SiAirbnb size={"48"} />
                    </Link>
                </Box>
                <HStack spacing={2}>
                    <IconButton onClick={toggleColorMode} variant={"ghost"} aria-label={"Toggle dark mode"} icon={Icon} />
                    <Button onClick={onOpen}>Log in</Button>
                    <Button colorScheme={"red"}>Sign up</Button>
                </HStack>
                <Modal onClose={onClose} isOpen={isOpen}>
                    <ModalOverlay />
                    <ModalContent>
                        <ModalHeader>Log in</ModalHeader>
                        <ModalCloseButton />
                        <ModalBody>
                            <VStack>
                                <InputGroup size={"md"}>
                                    <InputLeftElement children={
                                        <Box color="gray.500">
                                            <CiUser />
                                        </Box>
                                    } 
                                />
                                <Input variant={"filled"} placeholder="Username" />
                                </InputGroup>
                                <InputGroup>
                                    <InputLeftElement children={
                                        <Box color="gray.500">
                                            <CiDark />
                                        </Box>
                                    } />
                                    <Input variant={"filled"} placeholder="Password" type="password" />
                                </InputGroup>
                            </VStack>
                            <Button mt={4} colorScheme={"red"} width={"100%"}>
                                Log in
                            </Button>
                        </ModalBody>
                    </ModalContent>
                </Modal>
            </HStack>
            <Outlet />
        </Box>
    );
}