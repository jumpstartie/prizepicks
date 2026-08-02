/*
 * Sample PrizePicks MLB projections for the current slate.
 *
 * This is representative sample data that mirrors the shape of a PrizePicks
 * MLB projections feed. Because api.prizepicks.com is protected by a bot
 * challenge (DataDome / captcha) it cannot be fetched directly from the
 * browser or a plain server request, so the dashboard ships with a curated
 * slate. See the README ("Connecting real PrizePicks data") for how to swap
 * this array for a live feed.
 *
 * Each entry describes a single player prop as it appears on the PrizePicks
 * board:
 *   player     - player name
 *   team       - player's team abbreviation
 *   opponent   - opposing team abbreviation
 *   gameTime   - first pitch (local slate time), used only for display
 *   statType   - the PrizePicks stat category
 *   line       - the posted projection line
 *   projection - our model's projected value for the stat
 *   l10        - the player's average for the stat over the last 10 games
 *   matchupRank- opponent rank allowing this stat (1 = toughest, 30 = softest)
 */
const MLB_PROPS = [
  { player: "Aaron Judge", team: "NYY", opponent: "BOS", gameTime: "7:05 PM", statType: "Total Bases", line: 1.5, projection: 2.15, l10: 2.3, matchupRank: 24 },
  { player: "Shohei Ohtani", team: "LAD", opponent: "SD", gameTime: "9:10 PM", statType: "Total Bases", line: 1.5, projection: 2.05, l10: 2.1, matchupRank: 21 },
  { player: "Bobby Witt Jr.", team: "KC", opponent: "DET", gameTime: "8:10 PM", statType: "Hits+Runs+RBIs", line: 2.5, projection: 3.1, l10: 3.0, matchupRank: 27 },
  { player: "Gunnar Henderson", team: "BAL", opponent: "TB", gameTime: "7:05 PM", statType: "Hits+Runs+RBIs", line: 2.5, projection: 2.9, l10: 2.7, matchupRank: 18 },
  { player: "Juan Soto", team: "NYY", opponent: "BOS", gameTime: "7:05 PM", statType: "Hits", line: 1.5, projection: 1.05, l10: 1.1, matchupRank: 9 },
  { player: "Mookie Betts", team: "LAD", opponent: "SD", gameTime: "9:10 PM", statType: "Total Bases", line: 1.5, projection: 1.75, l10: 1.8, matchupRank: 16 },
  { player: "Freddie Freeman", team: "LAD", opponent: "SD", gameTime: "9:10 PM", statType: "Hits", line: 1.5, projection: 1.35, l10: 1.4, matchupRank: 20 },
  { player: "Corbin Carroll", team: "ARI", opponent: "COL", gameTime: "8:40 PM", statType: "Total Bases", line: 1.5, projection: 2.2, l10: 2.15, matchupRank: 29 },
  { player: "Kyle Tucker", team: "HOU", opponent: "SEA", gameTime: "8:10 PM", statType: "Hits+Runs+RBIs", line: 2.5, projection: 2.4, l10: 2.5, matchupRank: 7 },
  { player: "Marcus Semien", team: "TEX", opponent: "OAK", gameTime: "8:05 PM", statType: "Total Bases", line: 1.5, projection: 1.95, l10: 1.9, matchupRank: 25 },
  { player: "Yordan Alvarez", team: "HOU", opponent: "SEA", gameTime: "8:10 PM", statType: "Total Bases", line: 1.5, projection: 1.85, l10: 2.0, matchupRank: 12 },
  { player: "Vladimir Guerrero Jr.", team: "TOR", opponent: "CLE", gameTime: "7:07 PM", statType: "Hits", line: 1.5, projection: 1.4, l10: 1.45, matchupRank: 15 },
  { player: "Jose Ramirez", team: "CLE", opponent: "TOR", gameTime: "7:07 PM", statType: "Hits+Runs+RBIs", line: 2.5, projection: 2.85, l10: 2.8, matchupRank: 22 },
  { player: "Rafael Devers", team: "BOS", opponent: "NYY", gameTime: "7:05 PM", statType: "Total Bases", line: 1.5, projection: 1.7, l10: 1.65, matchupRank: 14 },
  { player: "Ronald Acuna Jr.", team: "ATL", opponent: "MIA", gameTime: "7:20 PM", statType: "Total Bases", line: 1.5, projection: 2.25, l10: 2.2, matchupRank: 26 },
  { player: "Elly De La Cruz", team: "CIN", opponent: "PIT", gameTime: "6:40 PM", statType: "Hits+Runs+RBIs", line: 2.5, projection: 3.0, l10: 2.95, matchupRank: 23 },
  { player: "Zack Wheeler", team: "PHI", opponent: "WSH", gameTime: "6:45 PM", statType: "Pitcher Strikeouts", line: 6.5, projection: 7.4, l10: 7.6, matchupRank: 28 },
  { player: "Tarik Skubal", team: "DET", opponent: "KC", gameTime: "8:10 PM", statType: "Pitcher Strikeouts", line: 7.5, projection: 8.3, l10: 8.5, matchupRank: 25 },
  { player: "Paul Skenes", team: "PIT", opponent: "CIN", gameTime: "6:40 PM", statType: "Pitcher Strikeouts", line: 6.5, projection: 7.2, l10: 7.1, matchupRank: 19 },
  { player: "Gerrit Cole", team: "NYY", opponent: "BOS", gameTime: "7:05 PM", statType: "Pitcher Strikeouts", line: 6.5, projection: 6.1, l10: 6.0, matchupRank: 8 },
  { player: "William Contreras", team: "MIL", opponent: "CHC", gameTime: "2:20 PM", statType: "Hits", line: 1.5, projection: 1.2, l10: 1.25, matchupRank: 11 },
  { player: "Fernando Tatis Jr.", team: "SD", opponent: "LAD", gameTime: "9:10 PM", statType: "Total Bases", line: 1.5, projection: 1.9, l10: 1.85, matchupRank: 17 },
  { player: "Adley Rutschman", team: "BAL", opponent: "TB", gameTime: "7:05 PM", statType: "Hits", line: 1.5, projection: 1.1, l10: 1.15, matchupRank: 10 },
  { player: "Francisco Lindor", team: "NYM", opponent: "ATL", gameTime: "7:10 PM", statType: "Hits+Runs+RBIs", line: 2.5, projection: 2.95, l10: 2.85, matchupRank: 21 },
];

if (typeof module !== "undefined" && module.exports) {
  module.exports = { MLB_PROPS };
}
