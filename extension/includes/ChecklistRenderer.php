<?php

declare( strict_types=1 );

namespace MediaWiki\Extension\WikiQA;

class ChecklistRenderer {
	private const ALLOWED_STATUSES = [ 'draft', 'ready', 'blocked' ];

	public static function render( object $parser, string $title = '', string $status = 'draft' ): array {
		if ( method_exists( $parser, 'getOutput' ) ) {
			$parser->getOutput()->addModules( [ 'ext.wikiQA.styles' ] );
		}

		$cleanTitle = trim( $title ) !== '' ? trim( $title ) : 'Quality checklist';
		$cleanStatus = self::normaliseStatus( $status );

		$html = sprintf(
			'<section class="wikiqa-checklist" data-status="%s"><h2>%s</h2><p class="wikiqa-checklist__status">Status: %s</p><ul><li>Acceptance criteria are documented.</li><li>Automated and manual coverage are linked.</li><li>Release evidence has an owner.</li></ul></section>',
			htmlspecialchars( $cleanStatus, ENT_QUOTES ),
			htmlspecialchars( $cleanTitle, ENT_QUOTES ),
			htmlspecialchars( ucfirst( $cleanStatus ), ENT_QUOTES )
		);

		return [ $html, 'isHTML' => true, 'noparse' => true ];
	}

	public static function normaliseStatus( string $status ): string {
		$cleanStatus = strtolower( trim( $status ) );
		return in_array( $cleanStatus, self::ALLOWED_STATUSES, true ) ? $cleanStatus : 'draft';
	}
}
