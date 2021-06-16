# document-scanner

# Description

This project is a prototype that attempts to improve on existing document readers for the blind. We have several goals for this including allowing it to automatically detect the alignment of a document and tell the user where it needs to be moved so the camera can see it, detecting sections of a document, summarizing a document and a full speech-based interface.

This is intended to be a proof-of-concept. As an app, this would first look around for text. If it saw none for a few seconds, then it would tell the user that it didn't see anything and to move the device and camera so that it could see the document. If it sees one out of alignment, then it will give the user directions such as "The document is to the right, could you move your camera to the right?" or "Could you move your camera away from what you are trying to scan?" among other potential directions. This is important as blind people have informed us that there is difficulty in knowing whether the camera is pointed in the right direction or not.

After this, it will look for specific ways to divide the document. This can include articles of a newspaper, sections of a menu, images and their captions, etc. The purpose of this is to allow the user to have only a specific portion of the document read off to them rather than the entire document.

Rest of description in progress

