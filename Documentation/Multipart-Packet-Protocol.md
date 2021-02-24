Multipart Packet Protocol
---

This protocol allows transportation of data larger than 65.5 KB (65535 Bytes) by splitting up the large data packet into multiple smaller packets.

Why 
--
Now, you might ask, why do we even need to do this? Why can't we just send the large data quantity over the network normally without splitting it up?

Well, if one is using the UDP socket protocol (as we are in this project), the maximum packet size for each UDP message is about 65.5 KB (65535 Bytes). Thus, if we need to transport data that is bigger than that size, we'll be out of luck. 

The implementation would be quite simple if we just split the raw data into multiple parts and then just put it in a json struct. However, this isn't very efficient. Thus, I have created this protocol to solve this issue.

How
--

We can solve this issue by break up the original data into multiple packets that the receiving end will put pack together. This allows the receiving end to reconstruct the original data. Let's call each group of packets needed to reconstruct the original data a "packet_group".

We can accomplish this by creating a packet structure like this:
`packet_group_id:num_of_packets_in_group:this_packet_num_in_group:[Raw Data]`

Let's go over in detail what each of these mean.

 - packet_group_id: This identifies which group this packet belongs to.
 - num_of_packets_in_group: This tells the receiver how many individual packets to look for in this group
 - this_packet_num_in_group: This tells the receiver what order the packets should be reassembled to recreate the original raw data.
 - [Raw Data]: This is part of the original data that was encoded.

Now that we have our packet structure, let's go over how we should encode the original raw data and how we should deal with putting the packets back together so that we can reassemble the original raw data.

