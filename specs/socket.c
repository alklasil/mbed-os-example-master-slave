#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>


#define MULTICAST_GROUP "ff15::ABBA:ABBA"
#define PORT 1234

int main(void)
{

    int s = socket(AF_INET6, SOCK_DGRAM, 0);

    struct sockaddr_in6 saddr;
    struct sockaddr_in6 addr_from;

    struct in6_addr mcast;
    if (inet_pton(AF_INET6, MULTICAST_GROUP, &mcast) != 1) {
        perror("inet_pton()");
        return 1;
    }

    saddr.sin6_family = AF_INET6;
    saddr.sin6_addr = in6addr_any;
    saddr.sin6_port = htons(PORT);
    if (bind(s, (struct sockaddr *)&saddr, sizeof saddr) == -1) {
        perror("bind()");
        return 1;
    }

    struct ipv6_mreq mreq = {
        .ipv6mr_multiaddr = mcast,
        .ipv6mr_interface = 0,
    };
    setsockopt(s, IPPROTO_IPV6, IPV6_JOIN_GROUP, &mreq, sizeof mreq);

    printf("Listening.\n");
    while (1) {
        char buf[100];
        socklen_t alen = sizeof addr_from;
        int len = recvfrom(s, buf, 100, 0, (struct sockaddr *)&addr_from, &alen);
        if (len == -1) {
            perror("recvfrom()");
            return -1;
        }
        printf("Received %s\n", buf);
    }
    close(s);
}

