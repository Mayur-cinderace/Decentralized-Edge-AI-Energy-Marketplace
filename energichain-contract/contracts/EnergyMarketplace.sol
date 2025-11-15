// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EnergyMarketplace {
    // Reentrancy guard state variable
    uint256 private locked = 1;

    // Reentrancy guard modifier
    modifier nonReentrant() {
        require(locked == 1, "No reentrancy");
        locked = 2;
        _;
        locked = 1;
    }
    // Struct to store offer details
    struct Offer {
        bool active;
        uint256 price;
        bytes32 userHash; // Hash of seller's identity or data
        address seller; // Seller's address
    }

    // Mapping to store offers by ID
    mapping(uint256 => Offer) public offers;
    // Mapping to store offer owners
    mapping(uint256 => address) public ownerOfOffer;

    // Event for when an offer is accepted
    event OfferAccepted(
        uint256 indexed offerId,
        address indexed buyer,
        bytes32 sellerHash,
        uint256 price,
        uint256 timestamp
    );

    // Function to accept an offer
    function acceptOffer(uint256 _id) external payable nonReentrant {
        // Check if offer exists and is active
        require(offers[_id].seller != address(0), "Offer does not exist");
        require(offers[_id].active, "Offer not active");
        require(msg.value == offers[_id].price, "Incorrect payment");
        require(msg.sender != ownerOfOffer[_id], "Cannot accept own offer");

        // Store offer data for effects
        Offer storage o = offers[_id];
        address seller = ownerOfOffer[_id];

        // Effects: Update state before external calls
        o.active = false;

        // Interaction: Transfer payment to seller
        payable(seller).transfer(msg.value);

        // Emit event
        emit OfferAccepted(_id, msg.sender, o.userHash, o.price, block.timestamp);
    }

    // Example function to create an offer (for testing)
    function createOffer(uint256 _id, uint256 _price, bytes32 _userHash) external {
        require(offers[_id].seller == address(0), "Offer ID already exists");
        offers[_id] = Offer({
            active: true,
            price: _price,
            userHash: _userHash,
            seller: msg.sender
        });
        ownerOfOffer[_id] = msg.sender;
    }
}