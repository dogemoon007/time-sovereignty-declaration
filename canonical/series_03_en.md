# A Protocol

The Theft of Time · Part 3 · Expanding Section V of the Declaration

> Someone has already written a different idea into a protocol and has been testing it on several chains since 2023. I treat it as one of many possible schemes of distribution. Its design has three layers.
> — The Sovereignty of Time

## A note on standpoint

Part 2 ended with a ruler: a basis of distribution independent of labor; capture and allocation separated; the three tests of consent; verifiability. This part applies it to one concrete thing.

I am not this protocol's spokesman and will not speak for it. I treat it as one of many possible schemes of distribution. I chose it to measure because it is one of the few attempts I know of that is already running on-chain with "existence," rather than labor or holding, as the basis of distribution. Once measured, you will see where it stands and where it is still only a statement. The outcome I would most like from this part is that you design a better one.

Its design has three layers. Take them in order.

## Layer one: proof of existence in time

For "who exists" to enter the ledger, two questions have to be answered first: how do you prove an existence is real, and how do you keep "existence" from becoming "identity"?

The first question has a name in cryptography: the Sybil attack — one person pretending to be a thousand. When Borge and colleagues proposed "proof of personhood" in 2017, the goal was exactly this: one person, one share, without a central identity authority. Three main routes have since emerged. Biometrics: use the iris or another physical trait to guarantee uniqueness, at the cost of a centralized collector and a key that cannot be replaced once leaked. Social graphs: let already-verified people vouch for one another, at the cost of collusion — a group can vouch non-existent people into existence. Liveness tests: require everyone to complete some machine-resistant task at the same moment, at the cost of tests failing one by one as machines improve. None of the three solves the problem completely. This is unsolved everywhere; it is not one protocol's failure.

The second question — existence is not identity — has a precise tool. In 1985, Goldwasser, Micali and Rackoff introduced zero-knowledge proofs: you can prove a statement true without revealing anything beyond the statement itself. Applied here: you can prove "I am a real existing person, and not any person already registered," without revealing who you are. Existence is recorded; identity is protected. This is not a theoretical possibility; it is technology in use.

The real design choice in this layer lies in the words "in time." Most proof-of-personhood schemes treat existence as a boolean — person or not — and then give one vote or one share per person. This protocol's credential accumulates over time: each period you are present, the ledger gains an entry. So "existence" turns from a yes/no question into a time series: the ledger records not "this is a person" but "this person was present during these periods." Time becomes the unit. That corresponds to the demand of Part 1 — time finally has a name on the ledger.

Its handling of the Sybil problem, as I understand it, is not a claim of solution but an engineering trade: accept that proof of existence cannot be perfect, then use the economics of the two layers above to make fabricated existence unprofitable — as long as the cost of faking one existence exceeds the share that existence can collect, faking loses money. That is a reasonable trade, not a mathematical proof. Whether it holds depends on the parameters of the other two layers, and parameters change. This is the first thing to watch.

Two confusions need clearing. It is not basic income. Basic income is a transfer: a capturer — a government, a foundation, or a company exchanging irises for tokens — puts up the money and pays per head; when the funder stops, the share stops. The existence credential is not a sum of money; it is a column on the ledger. Where the money comes from is the business of layer three; layer one only ensures that "who exists" gets recorded. Nor is it one-person-one-vote. Voting uses existence as a boolean; a credential that accumulates over time records existence as a quantity — how long you were present is how much is recorded. The former answers "are you a person"; the latter answers "where is your time." Those two distinctions set it apart from every proof-of-personhood project of the past decade: those projects prove people; this protocol records time.

## Layer two: a market for attention and creativity

Part 1 described an auction: buyers are advertisers, the seller is the platform, you are the lot. Layer two is still a market, with the parties changed: the seller is the person.

This idea has a lineage too. Lanier argued in *Who Owns the Future?* (2013) that every use of a person's data should earn its owner a micropayment. In 2018, Arrieta-Ibarra, Goff, Jiménez-Hernández, Lanier and Weyl sharpened it in the *AEA Papers and Proceedings* into a question: should we treat data as labor? If the raw material of machine learning is human output, then the people supplying it are workers and should be priced. In 2017, the Brave browser's Basic Attention Token made a partial implementation: users who viewed ads received a share of the revenue. It proved feasibility and exposed the limit — it remained inside the advertising frame, brokered by a platform, with users receiving a split the platform set.

This layer makes three design choices. Pricing power sits with the seller, not the platform — you decide what an hour of your attention is worth, and buyers take it or leave it. Only holders of existence credentials may sell — existence is the ticket of admission, and this is also layer one protecting layer two: machines cannot manufacture attention, because machines have no credential. Creativity and attention enter the same market — a work and a presence are two forms of the same thing, time.

Its problem is equally clear: a market needs buyers. A market with no buyers is a price tag. Who buys human attention and creativity? If the answer is "model companies that need human data to train on," then this layer and layer three are connected — the tax and the market are the same money flowing two ways. If there are no buyers, this layer is only a design. This is the second thing to watch.

## Layer three: an AI production tax

"Tax the machines" is not new. Gates proposed a robot tax in 2017: a robot that replaces a worker should pay taxes like one. Korinek has proposed an "AI dividend." California discussed a "data dividend" in 2019. All share one intuition: part of what machines amplify is public — the training data is the output of all humanity; no company created it — so the amplified part should not belong entirely to the amplifier.

One precedent deserves a look, because it has run for more than forty years: the Alaska Permanent Fund. Since 1982, Alaska has placed part of its oil revenue in a fund and paid every resident an annual dividend — one thousand dollars per person in 2025. Its logic matches this layer exactly: oil is value no one created, so it is distributed by existence rather than labor. Alaska's basis for the dividend is simply "you lived here for a year" — an administrative version of proof of existence in time.

This protocol's third layer differs from all of the above in two respects. First, the tax is not paid to a government; it is paid to holders of existence credentials. The reason is in Part 2: the state is a capturer too, and a tax that passes through the state has passed through a capturer's hands, so separation fails. Second, the base is "output amplified by machines," not the machines themselves — which sidesteps the robot tax's definitional problem (what counts as a robot?) at the price of another: what counts as "amplified by a machine"?

This layer has the most unsolved problems. Who sets the rate is a governance problem; how the base is measured is a technical problem; how an on-chain tax reaches off-chain output is a jurisdictional problem. To be plain: layer three is at present more a statement than a mechanism. It says where the money should come from and where it should go; it does not yet say how it is collected. This is the third thing to watch.

## Nearly four years of experiment

The protocol has run on several chains since 2023 and has been used by a few hundred strangers. What nearly four years prove and do not prove must be kept apart.

It has proven: that a basis of distribution independent of labor can be written as code; that it can be used by people who do not know one another; that it can survive nearly four years on several chains without depending on any institution. Before 2023 all three were conjectures.

It has not proven: scale — a few hundred people are not a few hundred million; Sybil resistance — no one has seriously attacked it, which is not the same as its withstanding attack; liquidity — nearly four years have not answered how a market prices when no buyers are present; legal standing — a protocol that pays "tax" to credential holders has no name yet in any jurisdiction.

One more thing must be said: there is a distance between design and deployment. Three layers are the design; what runs on-chain is an implementation, and an implementation need not cover the whole design. Readers should judge by on-chain facts, not by text. That applies to every protocol, including this one.

Measured by Part 2's ruler:

Basis independent of labor — holds in design. Its basis is existence in time.

Capture and allocation separated — holds in design. The tax does not pass through a capturer's hands; it goes directly to credential holders. But "in design" must be read with emphasis: if the rate is set by a few, allocation returns to some capturer's hands.

The three tests of consent — visibility holds; on-chain transfers are public. Zero-cost refusal partly holds; exit is easy, but entry requires first proving existence, and proof has a cost. Time as a ledger variable holds — this is its most fundamental difference from other schemes.

Verifiability — holds. Everything on-chain can be inspected by anyone.

Of the four marks, it passes all four in design and only "verifiable" in operation; the other three stop at "holds in design." That is its present position: a solution that can be verified, not a solution that has been proven.

## What could kill it

Since the standpoint is third-party, list the ways it could fail, in my order of likelihood.

The Sybil economics flip. Once the cost of faking an existence falls below the share that existence collects, faking turns from a loss into a profit, and the ledger would be flooded with false existences within weeks. Machines are making "a convincing fake presence" cheaper every year; that line approaches annually.

Capture of the rate. Who sets the layer-three rate is the thinnest point of the whole design. If a few holders decide, they will move the rate in their own favor; if the majority decides, the majority will vote itself a raise — both outcomes return allocation to some capturer's hands, and separation fails. No known governance mechanism avoids both at once.

No buyers. If layer two's market has only sellers for long enough, the credential is just a record with no path to redemption. The record has value in itself — it is time's name on the ledger — but a name that cannot be redeemed does not retain users.

Legal classification. An on-chain protocol that pays "tax" to credential holders will, in most jurisdictions, be classified as a security, a payment instrument, or a lottery, and any of the three would bar it from operating lawfully there. The protocol cannot solve this itself; it depends on people outside it.

The design–deployment gap. How many of the three layers are on-chain and how many remain in documents can only be checked on the chain, not learned from anyone's word.

Listing these five is not an attempt to talk the thing down. A scheme whose failure modes can be enumerated is more credible than one whose cannot — the former is a mechanism, the latter a faith.

## How to check a protocol

A method, in passing, that applies to any on-chain protocol claiming to solve distribution, not only this one. Open a block explorer and check five things. The contract's creation date — it decides whether "running for N years" is true. Holder and transfer counts — they decide whether "used by N people" is true. Whether the source is verified — it decides whether you can see what it actually does, rather than what it says it does. Who holds the admin keys — it decides whether separation is written into the code or into a promise; a protocol whose tax rate can be changed by a single key has separation only in its documentation. Where the tokens flow — it decides whether the "tax" really reaches credential holders or a handful of addresses. Check all five, and you will know more about the protocol than any article about it can tell you, including this one.

## Why there should be many

I said in Part 1 that the three thefts are not the work of three villains but a gap in the ledger. Closing the gap should not be the work of one scheme either.

The reason is the separation principle itself. If the world had a single protocol of distribution, it would be the sole allocator, and a sole allocator sooner or later becomes a capturer — precisely what separation exists to prevent. Competition among protocols of distribution is itself the guarantee of separation: with no single allocator, no one can enclose.

So this part ends not with a recommendation but an invitation. If you think one of the three layers is wrong, write your own version, measure it with the same ruler, and put it on a chain. The criteria are already here: a basis independent of labor, capture separated from allocation, the three tests of consent, verifiability. A scheme need not be perfect on all four, but it must answer all four.

Part 4 leaves the protocol and returns to the person. A ledger can record time, but what produces time is still a body that will die.

---

Fiat steals your past, algorithms steal your present, AI steals your future. Time sovereignty is taking all three back.

## Sources

- Borge, M., Kokoris-Kogias, E., Jovanovic, P., Gasser, L., Gailly, N., & Ford, B. (2017). "Proof-of-Personhood: Redemocratizing Permissionless Cryptocurrencies." *IEEE EuroS&PW*
- Goldwasser, S., Micali, S., & Rackoff, C. (1985). "The Knowledge Complexity of Interactive Proof-Systems." *STOC*
- Lanier, J. (2013). *Who Owns the Future?*
- Arrieta-Ibarra, I., Goff, L., Jiménez-Hernández, D., Lanier, J., & Weyl, E. G. (2018). "Should We Treat Data as Labor?" *AEA Papers and Proceedings* 108
- Brave Software (2017). Basic Attention Token whitepaper
- Gates, B. (2017). Interview on taxing robots, *Quartz*
- Korinek, A., & Stiglitz, J. E. (2017). NBER Working Paper 24174
- Alaska Permanent Fund Dividend: since 1982; $1,000 per person in 2025 ([Alaska's News Source](https://www.alaskasnewssource.com/2025/09/10/first-2025-pfd-be-paid-oct-2/))
- The protocol itself: judge by its on-chain contracts and transaction records; its name and address are deliberately omitted here so that this part cannot be read as promotion
