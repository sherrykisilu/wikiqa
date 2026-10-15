<?php

declare( strict_types=1 );

namespace MediaWiki\Extension\WikiQA;

class Hooks {
	public static function onParserFirstCallInit( object $parser ): bool {
		$parser->setFunctionHook( 'qaChecklist', [ ChecklistRenderer::class, 'render' ] );
		return true;
	}
}
