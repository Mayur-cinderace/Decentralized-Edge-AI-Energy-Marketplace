// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EnergyOffer {
    struct Offer {
        bytes32 userHash;
        uint256 price;
        uint256 timestamp;
        bool active;
    }

    uint256 public constant MIN_PRICE = 0.01 ether;
    Offer[] public offers;
    mapping(bytes32 => uint256[]) public userOffers;
    mapping(uint256 => address) public ownerOfOffer;

    event OfferCreated(
        uint256 indexed offerId,
        bytes32 indexed userHash,
        uint256 price,
        uint256 timestamp
    );
    event OfferAccepted(
        uint256 indexed offerId,
        address buyer,
        bytes32 sellerHash,
        uint256 price,
        uint256 timestamp
    );
    event OfferCancelled(
        uint256 indexed offerId,
        bytes32 indexed userHash
    );

    function createOffer(bytes32 _userHash, uint256 _price) external {
        require(_price >= MIN_PRICE, "Price below minimum");
        uint256 id = offers.length;
        offers.push(Offer({
            userHash: _userHash,
            price: _price,
            timestamp: block.timestamp,
            active: true
        }));
        userOffers[_userHash].push(id);
        ownerOfOffer[id] = msg.sender;
        emit OfferCreated(id, _userHash, _price, block.timestamp);
    }

    function getOfferCount() external view returns (uint256) {
        return offers.length;
    }

    function getOffer(uint256 _id) external view returns (
        bytes32 userHash,
        uint256 price,
        uint256 timestamp,
        bool active
    ) {
        require(_id < offers.length, "Invalid offer ID");
        Offer memory o = offers[_id];
        return (o.userHash, o.price, o.timestamp, o.active);
    }

    function cancelOffer(uint256 _id) external {
        require(_id < offers.length, "Invalid offer ID");
        require(offers[_id].active, "Offer already inactive");
        require(ownerOfOffer[_id] == msg.sender, "Not offer owner");
        offers[_id].active = false;
        emit OfferCancelled(_id, offers[_id].userHash);
    }

    function acceptOffer(uint256 _id) external payable {
        require(_id < offers.length, "Invalid offer ID");
        Offer storage o = offers[_id];
        require(o.active, "Offer not active");
        require(msg.value == o.price, "Incorrect payment");
        require(ownerOfOffer[_id] != msg.sender, "Cannot accept own offer");
        
        o.active = false;
        
        // Transfer payment to offer creator
        (bool success, ) = payable(ownerOfOffer[_id]).call{value: msg.value}("");
        require(success, "Transfer failed");
        
        emit OfferAccepted(_id, msg.sender, o.userHash, o.price, block.timestamp);
    }

    function getActiveUserOfferIds(bytes32 _userHash) external view returns (uint256[] memory) {
        uint256[] memory all = userOffers[_userHash];
        uint256 len = 0;
        for (uint256 i = 0; i < all.length; i++) {
            if (all[i] < offers.length && offers[all[i]].active) {
                len++;
            }
        }
        uint256[] memory active = new uint256[](len);
        uint256 idx = 0;
        for (uint256 i = 0; i < all.length; i++) {
            if (all[i] < offers.length && offers[all[i]].active) {
                active[idx] = all[i];
                idx++;
            }
        }
        return active;
    }

    function getOwnerAddress(uint256 _id) external view returns (address) {
        require(_id < offers.length, "Invalid offer ID");
        return ownerOfOffer[_id];
    }
}