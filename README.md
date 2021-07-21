# document-scanner

This is a research project intended to help people who are blind. This project is a work in progress and we have much of the project described below. At it's core, it is a document reader. By document, we mean anything with text, and not just traditional documents.

# Description

This project is a prototype that attempts to improve on existing document readers for the blind. We have several goals for this including allowing it to automatically detect the alignment of a document and tell the user where it needs to be moved so the camera can see it, detecting sections of a document, summarizing a document and a full speech-based interface.

This is intended to be a proof-of-concept. As an app, this would first look around for text. If it saw none for a few seconds, then it would tell the user that it didn't see anything and to move the device and camera so that it could see the document. If it sees one out of alignment, then it will give the user directions such as "The document is to the right, could you move your camera to the right?" or "Could you move your camera away from what you are trying to scan?" among other potential directions. This is important as blind people have informed us that there is difficulty in knowing whether the camera is pointed in the right direction or not.

After this, it will look for specific ways to divide the document. This can include articles of a newspaper, sections of a menu, images and their captions, etc. The purpose of this is to allow the user to have only a specific portion of the document read off to them rather than the entire document. This is also useful because we have heard blind people complain that current related technologies will read off text in ways that are not chronological, i.e. they could read off an image caption in the middle of a paragraph. By having the document read by section rather than all at once, we can have a document reader that makes sense to the user. 

As mentioned earlier, all of this will be done with a speech-based interface. We choose this because it is the most intuitive type of interface for blind individuals. There are a few other components that will allow other functionality for this, which are described up ahead. These features will be added to this project though the speech interface

This project may also include a barcode scanner. This will allow the user to get information about a product if we hook this prototype up to some external database. This could work in situations where the product is round, but the barcode can be easily scanned by the device's camera. This may not work in situations where the barcode is partially hidden.

This prototype may also include some mechanism to summarize documents so that the user. This will hopefully be of good use as an alternative to skimming through a document. The implementation of this is still tbd.


