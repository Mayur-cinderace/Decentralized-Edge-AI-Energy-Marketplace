// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EnergyOffer {
    struct Offer {
        bytes32 userHash;     // keccak256(username)
        uint256 price;        // in wei (or your token decimals)
        uint256 timestamp;
        bool active;
    }

    uint256 public constant MIN_PRICE = 0.01 ether;   // floor price – change as needed

    Offer[] public offers;
    mapping(bytes32 => uint256[]) public userOffers; // userHash => array of offer indices

    event OfferCreated(
        uint256 indexed offerId,
        bytes32 indexed userHash,
        uint256 price,
        uint256 timestamp
    );

    /// @dev Create a new energy offer. Price must be >= MIN_PRICE.
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
        emit OfferCreated(id, _userHash, _price, block.timestamp);
    }

    /// @dev Get total number of offers
    function getOfferCount() external view returns (uint256) {
        return offers.length;
    }

    /// @dev Get a specific offer (read-only)
    function getOffer(uint256 _id) external view returns (
        bytes32 userHash,
        uint256 price,
        uint256 timestamp,
        bool active
    ) {
        Offer memory o = offers[_id];
        return (o.userHash, o.price, o.timestamp, o.active);
    }

    /// @dev Deactivate an offer (optional – you can expand)
    function cancelOffer(uint256 _id) external {
        require(offers[_id].active, "Already inactive");
        // In a real marketplace you would check msg.sender == owner
        offers[_id].active = false;
    }
}