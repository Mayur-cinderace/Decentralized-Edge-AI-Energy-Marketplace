event OfferAccepted(
    uint256 indexed offerId,
    address buyer,
    bytes32 sellerHash,
    uint256 price,
    uint256 timestamp
);



function acceptOffer(uint256 _id) external payable {
  Offer storage o = offers[_id];
  require(o.active, "Offer not active");
  require(msg.value == o.price, "Incorrect payment");
  require(msg.sender != ownerOfOffer[_id], "Cannot accept own offer");
  
  o.active = false;
  payable(ownerOfOffer[_id]).transfer(msg.value);
  
  emit OfferAccepted(_id, msg.sender, o.userHash, o.price, block.timestamp);
}

