// omni_creator_phaser_studio_ui.dart
// Creator Suite coupled with Phaser Studio UI (Flutter / Dart)
// Complete Mini-Game Modding, Tilemap Inspector, Asset Packager & P2P Tipping Monetization Workbench

import 'package:flutter/material.dart';

class CreatorPhaserStudioScreen extends StatefulWidget {
  const CreatorPhaserStudioScreen({super.key});

  @override
  State<CreatorPhaserStudioScreen> createState() => _CreatorPhaserStudioScreenState();
}

class _CreatorPhaserStudioScreenState extends State<CreatorPhaserStudioScreen> {
  int _selectedTabIndex = 0;

  final List<Map<String, dynamic>> _myMods = [
    {
      'mod_id': 'mod_asteroids_v2',
      'name': 'Deep Space Vector Blaster',
      'type': 'Phaser 2D Arcade',
      'version': '1.2.0',
      'downloads': 142,
      'tips_earned': 4500, // cents ($45.00)
      'status': 'Published to Mesh',
    },
    {
      'mod_id': 'mod_plaza_fighter',
      'name': 'Plaza Brawler Cyber Armor',
      'type': 'LPE 2D Cosmetic',
      'version': '0.9.1',
      'downloads': 89,
      'tips_earned': 2800, // cents ($28.00)
      'status': 'Local Draft',
    },
  ];

  final List<String> _phaserTemplates = [
    '2D Retro Arcade Shooter (Asteroids)',
    'Tactical Grid 9x9 Strategy',
    'Phaser Platformer & Tilemap World',
    'LPE Avatar Cosmetic Layer Pack',
  ];

  String _selectedTemplate = '2D Retro Arcade Shooter (Asteroids)';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        backgroundColor: const Color(0xFF1E293B),
        elevation: 0,
        title: Row(
          children: const [
            Icon(Icons.gamepad, color: Colors.tealAccent, size: 22),
            SizedBox(width: 10),
            Text(
              'Creators Suite & Phaser Studio',
              style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 18),
            ),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.build_circle_outlined, color: Colors.tealAccent),
            onPressed: () => _showBuildManifestModal(context),
          ),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            // Top Workspace Navigation Tabs
            Container(
              color: const Color(0xFF1E293B),
              child: Row(
                children: [
                  _buildNavTab(0, 'My Mods & Games', Icons.folder_special_outlined),
                  _buildNavTab(1, 'Phaser 2D Studio', Icons.design_services),
                  _buildNavTab(2, 'Monetization & Tips', Icons.monetization_on_outlined),
                ],
              ),
            ),

            Expanded(
              child: IndexedStack(
                index: _selectedTabIndex,
                children: [
                  _buildMyModsView(),
                  _buildPhaserStudioView(),
                  _buildMonetizationView(),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildNavTab(int index, String title, IconData icon) {
    final isSelected = _selectedTabIndex == index;
    return Expanded(
      child: InkWell(
        onTap: () => setState(() => _selectedTabIndex = index),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 12),
          decoration: BoxDecoration(
            border: Border(
              bottom: BorderSide(
                color: isSelected ? Colors.tealAccent : Colors.transparent,
                width: 2.5,
              ),
            ),
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(icon, color: isSelected ? Colors.tealAccent : Colors.white54, size: 20),
              const SizedBox(height: 4),
              Text(
                title,
                style: TextStyle(
                  color: isSelected ? Colors.tealAccent : Colors.white54,
                  fontSize: 11,
                  fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  // TAB 1: My Mods & Games
  Widget _buildMyModsView() {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const Text(
              'My Created Projects (.omnimod)',
              style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
            ),
            ElevatedButton.icon(
              onPressed: () => setState(() => _selectedTabIndex = 1),
              icon: const Icon(Icons.add, size: 16),
              label: const Text('Create New'),
              style: ElevatedButton.styleFrom(backgroundColor: Colors.tealAccent, foregroundColor: Colors.black),
            ),
          ],
        ),
        const SizedBox(height: 14),
        ..._myMods.map((mod) => Container(
              margin: const EdgeInsets.only(bottom: 12),
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: const Color(0xFF1E293B),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Colors.white10),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        mod['name'],
                        style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                        decoration: BoxDecoration(
                          color: mod['status'] == 'Published to Mesh' ? Colors.teal.withOpacity(0.2) : Colors.amber.withOpacity(0.2),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Text(
                          mod['status'],
                          style: TextStyle(
                            color: mod['status'] == 'Published to Mesh' ? Colors.tealAccent : Colors.amberAccent,
                            fontSize: 11,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 6),
                  Text(
                    'Type: ${mod['type']} | Version: ${mod['version']}',
                    style: const TextStyle(color: Colors.white54, fontSize: 12),
                  ),
                  const Divider(color: Colors.white10, height: 20),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        'P2P Downloads: ${mod['downloads']}',
                        style: const TextStyle(color: Colors.white70, fontSize: 12),
                      ),
                      Text(
                        'Tips Earned: \$${(mod['tips_earned'] / 100).toStringAsFixed(2)}',
                        style: const TextStyle(color: Colors.tealAccent, fontWeight: FontWeight.bold, fontSize: 13),
                      ),
                    ],
                  ),
                ],
              ),
            )),
      ],
    );
  }

  // TAB 2: Phaser 2D Studio & Mod Builder
  Widget _buildPhaserStudioView() {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        const Text(
          'Phaser 2D Modding Workbench',
          style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 6),
        const Text(
          'Select a base template to customize sprites, audio synth curves, and game logic rules.',
          style: TextStyle(color: Colors.white54, fontSize: 12),
        ),
        const SizedBox(height: 16),

        // Template Dropdown Selector
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 12),
          decoration: BoxDecoration(
            color: const Color(0xFF1E293B),
            borderRadius: BorderRadius.circular(10),
            border: Border.all(color: Colors.tealAccent.withOpacity(0.5)),
          ),
          child: DropdownButtonHideUnderline(
            child: DropdownButton<String>(
              value: _selectedTemplate,
              dropdownColor: const Color(0xFF1E293B),
              isExpanded: true,
              style: const TextStyle(color: Colors.white, fontSize: 13),
              items: _phaserTemplates.map((t) => DropdownMenuItem(value: t, child: Text(t))).toList(),
              onChanged: (val) => setState(() => _selectedTemplate = val!),
            ),
          ),
        ),

        const SizedBox(height: 20),

        // Interactive Studio Controls Mockup
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: const Color(0xFF1E293B),
            borderRadius: BorderRadius.circular(14),
            border: Border.all(color: Colors.white10),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Canvas & Assets Configuration', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
              const SizedBox(height: 12),
              _buildConfigSlider('Game Speed Multiplier', 1.0, 0.5, 3.0),
              _buildConfigSlider('Player Health Pool', 100.0, 50.0, 500.0),
              _buildConfigSlider('Enemy Spawn Frequency (sec)', 2.5, 0.5, 5.0),
              const SizedBox(height: 12),
              ElevatedButton.icon(
                onPressed: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Building .omnimod package with Ed25519 Merkle Root signature...')),
                  );
                },
                icon: const Icon(Icons.inventory_2_outlined),
                label: const Text('Compile & Package .omnimod'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.tealAccent,
                  foregroundColor: Colors.black,
                  minimumSize: const Size(double.infinity, 44),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildConfigSlider(String label, double value, double min, double max) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(label, style: const TextStyle(color: Colors.white70, fontSize: 12)),
            Text(value.toStringAsFixed(1), style: const TextStyle(color: Colors.tealAccent, fontSize: 12, fontWeight: FontWeight.bold)),
          ],
        ),
        Slider(
          value: value,
          min: min,
          max: max,
          activeColor: Colors.tealAccent,
          inactiveColor: Colors.white10,
          onChanged: (_) {},
        ),
      ],
    );
  }

  // TAB 3: Monetization & P2P Tipping
  Widget _buildMonetizationView() {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        const Text(
          'Creator Monetization & Test Credit Tipping',
          style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 6),
        const Text(
          'Direct P2P micro-tips sent to your author public key when users play or download your mods.',
          style: TextStyle(color: Colors.white54, fontSize: 12),
        ),
        const SizedBox(height: 16),

        Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            color: const Color(0xFF1E293B),
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: Colors.tealAccent.withOpacity(0.4)),
          ),
          child: Column(
            children: const [
              Text('Total Creator Revenue Balance', style: TextStyle(color: Colors.white70, fontSize: 13)),
              SizedBox(height: 8),
              Text('\$73.00 Test Credits', style: TextStyle(color: Colors.tealAccent, fontSize: 28, fontWeight: FontWeight.bold)),
              SizedBox(height: 4),
              Text('7,300 Cents | 0.00 Platform Fee', style: TextStyle(color: Colors.white38, fontSize: 11)),
            ],
          ),
        ),
      ],
    );
  }

  void _showBuildManifestModal(BuildContext context) {
    showModalBottomSheet(
      context: context,
      backgroundColor: const Color(0xFF1E293B),
      builder: (_) => Container(
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: const [
            Text('Mod Package Manifest (.omnimod)', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16)),
            SizedBox(height: 12),
            Text('Manifest Version: 1.0.0', style: TextStyle(color: Colors.white70, fontSize: 13)),
            Text('Publisher Key: 0xc065885521c1ffb54fa9c1153b710c2f...', style: TextStyle(color: Colors.white38, fontSize: 11)),
            Text('Target Engine: Phaser 4 / Flutter GPU', style: TextStyle(color: Colors.tealAccent, fontSize: 12)),
          ],
        ),
      ),
    );
  }
}
