
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

`packet_group_id:group_packet_size:group_packet_num:[Raw Data]`

Let's go over in detail what each of these mean.

 - `packet_group_id`: This `integer` identifies which group this packet belongs to. If you are sending a large quantity of group of packets, then this number might overflow. Thus, in order to prevent that from happening, the maximum number this packet can reach is `128`. However, this raises the concern that if you send `128` incomplete packet groups, the incoming packets will overlap groups. The solution to this can be found in the *Unpacking / Decoding* section.
 - `group_packet_size`: This `integer` tells the receiver how many individual packets to look for in this group. This will range from `1` to any number but should never be `0`.
 - `group_packet_num`: This `integer` tells the receiver what order the packets should be reassembled to recreate the original raw data. To keep everything standarized, this number will start at `0` for the first packet and increment by `1`.
 - `[Raw Data]`: This `string` is part of the original data that was encoded.

Now that we have our packet structure, let's go over how we should encode the original raw data and how we should deal with putting the packets back together so that we can reassemble the original raw data.

Packing / Encoding
--
Let's first deal with how we should encode the raw data for sending. 

We first need to intake the raw data and check if it even exceeds our imposed limit of around 65 KB. If it doesn't, then we don't need to split up the raw data at all. We can just send the packet with the aforementioned structure  but instead, it would have `1` for `group_packet_size` and `0` for `group_packet_num`.

If the raw data does exceed 65 KB, then we need to split it up. We can accomplish this by having a buffer that will act as one indivdual packet. We will then iterate through the raw data's bytes and copy over the bytes into the buffer until it reaches the maximum size limit. Once the buffer reaches it's maximum size limit, we can add it to the a queue or an array to be sent out. Rinse and repeat until you have an array of packets that need to be sent out. 

Now, to determine the `packet_group_id`, you should keep a variable of the number of packet groups you have sent out. Once this reaches the maximum number of `128`, you should set it back to zero in order to restart. An efficent way of doing this would be to use the modulo operator, `%`. This way, the number never actually reaches `128` but caps out at `127` instead.

Then, using your preferred method of communication, you can send the array of packets.

Unpacking / Decoding
--
Let's deal with how we should decode the packets so that we can reconstruct our raw data.

Since UDP doesn't guarentee packet delivery or order, we need to be able to deal with this when reconstructing our data. 

When receiving a stream of UDP packets, we can pass these raw packets to a class that should deal with these packets and reconstruct our orignal data. Once it has the original data, the class can use a callback to your other class to deal with the original data.

The main flow of this class should go like this:

 - Receive packet
 - Pass packet to function in class
 - Check `packet_group_id` to see if any previous packets have been received. 
	 - If any previous packets have been received, add the raw data to the array corresponding to the id. You must add the raw data in the order specified in `group_packet_num`.
	 - If there aren't any previous packets that were received, create a new array corresponding to the id with size `packet_group_size` and add the raw data in the order specified in `group_packet_num`
 - Now, we check if any arrays have reached their `packet_group_size`. We don't actually need to check every array over and over again but instead, all we have to do is check the array that corresponds to the packet that we just received by using `packet_group_id`.
	 - If the array has reached the size limit, all you need to do to reconstruct the raw data is just iterate through the array and append.
	 	- Next, if you would like to, you can just discard all other arrays and start fresh. However, the issue with this is that you might skip entire packet groups.

